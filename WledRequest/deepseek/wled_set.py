#!/usr/bin/env python3
"""
WLED Color Setter – Steuert ein oder mehrere WLED-Geräte per HTTP JSON API.

Unterstützt RGB-Werte und Farbnamen. Liest Standard-IPs und -Farbe aus
einer ``config.json``. CLI-Argumente überschreiben die Konfiguration.

Usage:
    python3 wled_set.py
    python3 wled_set.py -c rot
    python3 wled_set.py -c "255 0 0"
    python3 wled_set.py -i "192.168.2.125,192.168.2.169" -c blau
    python3 wled_set.py -i "192.168.2.125" -c grün -s
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List, Optional

import requests

# ---------------------------------------------------------------------------
# Pfade & Konstanten
# ---------------------------------------------------------------------------

CONFIG_FILE = Path(__file__).parent / "config.json"
LOG_FILE = Path(__file__).parent / "wled_set.log"

# Farbnamen → RGB (dient als switch/case-Ersatz)
COLOR_NAME_MAP = {
    "rot":    [255,   0,   0],
    "grün":   [  0, 255,   0],
    "gruen":  [  0, 255,   0],
    "blau":   [  0,   0, 255],
    "orange": [255, 120,   0],
    "weiß":   [255, 255, 255],
    "weiss":  [255, 255, 255],
    "gelb":   [255, 255,   0],
}

VALID_COLOR_NAMES = sorted(set(COLOR_NAME_MAP.keys()))

DEFAULT_CONFIG = {
    "ips": ["192.168.2.169"],
    "default_color": [255, 0, 0],
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

# Root-Logger auf niedrigstes Level (alles durchlassen)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Formatter (für beide Handler gleich)
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)

# 1. File-Handler – speichert ALLES (ab DEBUG)
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# 2. Stream-Handler – zeigt nur WARNING und höher im Terminal
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.WARNING)   # ← HIER das Terminal-Level
console_handler.setFormatter(formatter)

# Handler an den Logger hängen
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# ---------------------------------------------------------------------------
# Konfiguration laden / speichern
# ---------------------------------------------------------------------------


def load_config(config_path: Path = CONFIG_FILE) -> dict:
    """Lädt die Konfiguration aus einer JSON-Datei.

    Falls die Datei nicht existiert oder kaputt ist, wird die
    ``DEFAULT_CONFIG`` zurückgegeben.

    Args:
        config_path: Pfad zur JSON-Konfigurationsdatei.

    Returns:
        Dictionary mit ``ips`` (list) und ``default_color`` (list).
    """
    if not config_path.exists():
        logger.warning(
            "Konfigurationsdatei '%s' nicht gefunden – verwende Defaults.",
            config_path,
        )
        return DEFAULT_CONFIG.copy()

    try:
        with open(config_path, "r", encoding="utf-8") as fh:
            config = json.load(fh)
        logger.info("Konfiguration aus '%s' geladen.", config_path)
        return config
    except (json.JSONDecodeError, OSError) as exc:
        logger.error(
            "Fehler beim Laden von '%s': %s – verwende Defaults.",
            config_path,
            exc,
        )
        return DEFAULT_CONFIG.copy()


def save_config(
    ips: List[str],
    color: List[int],
    config_path: Path = CONFIG_FILE,
) -> None:
    """Speichert IPs und Farbe dauerhaft in die config.json.

    Args:
        ips: Liste von IP-Adressen (str).
        color: RGB-Liste, z. B. ``[255, 0, 0]``.
        config_path: Zielpfad der Konfigurationsdatei.
    """
    config = {"ips": ips, "default_color": color}
    try:
        with open(config_path, "w", encoding="utf-8") as fh:
            json.dump(config, fh, indent=4, ensure_ascii=False)
        logger.info("Konfiguration gespeichert: ips=%s, color=%s", ips, color)
        print(f"✅ Konfiguration nach {config_path} gespeichert.")
    except OSError as exc:
        logger.error("Fehler beim Speichern der Konfiguration: %s", exc)
        print(f"❌ Fehler beim Speichern: {exc}")


# ---------------------------------------------------------------------------
# Farb-Parsing
# ---------------------------------------------------------------------------


def parse_color(color_arg: str) -> List[int]:
    """Wandelt eine Farbangabe in RGB-Werte um.

    Zwei Formate werden unterstützt:

    1. **RGB**: Drei durch Leerzeichen getrennte Integer (0–255),
       z. B. ``"255 0 0"``.
    2. **Farbname**: Einer der vordefinierten Namen, z. B. ``"rot"``,
       ``"blau"`` (siehe ``COLOR_NAME_MAP``).

    Args:
        color_arg: Farbangabe als String.

    Returns:
        RGB-Liste ``[R, G, B]`` mit Werten 0–255.

    Raises:
        ValueError: Wenn die Angabe weder als RGB noch als Farbname
            interpretiert werden kann.
    """
    # Versuch 1: RGB-Zahlen (z. B. "255 0 0")
    parts = color_arg.strip().split()
    if len(parts) == 3:
        try:
            rgb = [int(p) for p in parts]
            for val in rgb:
                if not 0 <= val <= 255:
                    raise ValueError(
                        f"RGB-Wert {val} liegt nicht im Bereich 0–255."
                    )
            return rgb
        except ValueError:
            pass  # → weitermachen mit Farbnamen

    # Versuch 2: Farbname (switch/case-Äquivalent via dict)
    color_lower = color_arg.strip().lower()
    if color_lower in COLOR_NAME_MAP:
        return COLOR_NAME_MAP[color_lower]

    # Nichts passt
    raise ValueError(
        f"Ungültige Farbangabe: '{color_arg}'. "
        f"Erwartet: drei RGB-Werte (0–255) oder einen Farbnamen "
        f"({', '.join(VALID_COLOR_NAMES)})."
    )


# ---------------------------------------------------------------------------
# WLED-Controller (ein Gerät)
# ---------------------------------------------------------------------------


class WLEDController:
    """Steuert ein einzelnes WLED-Gerät via HTTP JSON API.

    Attributes:
        ip: IP-Adresse des WLED-Geräts (str).
        base_url: Zusammengesetzte URL für State-Requests (str).
        timeout: Request-Timeout in Sekunden (int).
    """

    def __init__(self, ip: str, timeout: int = 5) -> None:
        """Initialisiert den Controller.

        Args:
            ip: IP-Adresse des Geräts, z. B. ``"192.168.2.169"``.
            timeout: Timeout für HTTP-Requests in Sekunden.
        """
        self.ip = ip
        self.base_url = f"http://{ip}/json/state"
        self.timeout = timeout

    def set_color(self, rgb: List[int], brightness: int = 255) -> bool:
        """Sendet Farbe und Helligkeit an das WLED-Gerät.

        Args:
            rgb: Farbwerte ``[R, G, B]`` (je 0–255).
            brightness: Helligkeit 0–255 (Default: 255).

        Returns:
            ``True`` bei Erfolg, sonst ``False``.
        """
        payload = {
            "on": True,
            "bri": brightness,
            "seg": [{"col": [rgb]}],
        }

        try:
            response = requests.post(
                self.base_url,
                json=payload,
                timeout=self.timeout,
            )

            if response.status_code == 200:
                logger.info(
                    "✅ %s → Farbe %s, Helligkeit %s gesetzt.",
                    self.ip,
                    rgb,
                    brightness,
                )
                return True

            logger.error(
                "❌ %s → HTTP %s – %s",
                self.ip,
                response.status_code,
                response.text.strip(),
            )
            return False

        except requests.exceptions.Timeout:
            logger.error("❌ %s → Timeout nach %s s.", self.ip, self.timeout)
            return False
        except requests.exceptions.ConnectionError as exc:
            logger.error("❌ %s → Verbindungsfehler: %s", self.ip, exc)
            return False
        except requests.exceptions.RequestException as exc:
            logger.error("❌ %s → Fehler: %s", self.ip, exc)
            return False

    def get_state(self) -> Optional[dict]:
        """Fragt den aktuellen Zustand des Geräts ab.

        Returns:
            JSON-Dictionary oder ``None`` bei Fehler.
        """
        try:
            response = requests.get(self.base_url, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            logger.error(
                "Status-Abfrage %s → HTTP %s",
                self.ip,
                response.status_code,
            )
            return None
        except requests.exceptions.RequestException as exc:
            logger.error("Status-Abfrage %s fehlgeschlagen: %s", self.ip, exc)
            return None


# ---------------------------------------------------------------------------
# WLED-Manager (mehrere Geräte)
# ---------------------------------------------------------------------------


class WLEDManager:
    """Verwaltet mehrere :class:`WLEDController` und setzt sie gemeinsam.

    Attributes:
        controllers: Liste von WLEDController-Instanzen.
    """

    def __init__(self, ips: List[str]) -> None:
        """Erzeugt für jede IP einen eigenen Controller.

        Args:
            ips: Liste von IP-Adressen (str).
        """
        self.controllers = [WLEDController(ip.strip()) for ip in ips]
        logger.info(
            "Manager initialisiert mit %d Gerät(en): %s",
            len(self.controllers),
            [c.ip for c in self.controllers],
        )

    def set_all(self, rgb: List[int], brightness: int = 255) -> bool:
        """Setzt alle verwalteten Geräte auf dieselbe Farbe.

        Args:
            rgb: RGB-Werte ``[R, G, B]``.
            brightness: Helligkeit 0–255.

        Returns:
            ``True`` wenn **alle** Geräte erfolgreich waren.
        """
        results = [ctrl.set_color(rgb, brightness) for ctrl in self.controllers]
        all_ok = all(results)

        if all_ok:
            logger.info("🎨 Alle %d Gerät(e) auf %s gesetzt.", len(results), rgb)
        else:
            failed = sum(1 for ok in results if not ok)
            logger.warning(
                "⚠️ %d von %d Gerät(en) konnten nicht gesetzt werden.",
                failed,
                len(results),
            )
        return all_ok


# ---------------------------------------------------------------------------
# CLI / ArgumentParser
# ---------------------------------------------------------------------------


def build_argument_parser() -> argparse.ArgumentParser:
    """Baut den ArgumentParser mit allen Optionen.

    Returns:
        Fertig konfigurierter :class:`argparse.ArgumentParser`.
    """
    parser = argparse.ArgumentParser(
        prog="wled_set.py",
        description=(
            "Setzt die Farbe von einem oder mehreren WLED-Geräten. "
            "Ohne Argumente werden IPs und Farbe aus der config.json gelesen."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Beispiele:\n"
            "  python3 wled_set.py\n"
            "  python3 wled_set.py -c rot\n"
            '  python3 wled_set.py -c "255 128 0"\n'
            '  python3 wled_set.py -i "192.168.2.125,192.168.2.169" -c blau\n'
            '  python3 wled_set.py -i "192.168.2.125" -c grün -s'
        ),
    )

    parser.add_argument(
        "-i",
        "--inventory",
        type=str,
        default=None,
        help=(
            "Komma-getrennte IP-Liste, z. B. "
            '"192.168.2.125,192.168.2.169". '
            "Ohne Angabe werden die IPs aus config.json verwendet."
        ),
    )

    parser.add_argument(
        "-c",
        "--color",
        type=str,
        default=None,
        help=(
            "Farbe als RGB (z. B. \"255 0 0\") oder Farbname "
            f"({', '.join(VALID_COLOR_NAMES)}). "
            "Ohne Angabe wird default_color aus config.json verwendet."
        ),
    )

    parser.add_argument(
        "-s",
        "--save",
        action="store_true",
        help="Speichert die angegebenen IPs und Farbe in der config.json.",
    )

    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Hauptfunktion: CLI parsen, Konfiguration laden, Farbe setzen."""
    parser = build_argument_parser()
    args = parser.parse_args()

    # ── Konfiguration laden ───────────────────────────────────────────
    config = load_config()

    # ── IPs ermitteln ──────────────────────────────────────────────────
    if args.inventory is not None:
        ips = [ip.strip() for ip in args.inventory.split(",") if ip.strip()]
        if not ips:
            logger.error("Keine gültigen IP-Adressen angegeben.")
            sys.exit(1)
    else:
        ips = config.get("ips", DEFAULT_CONFIG["ips"])

    # ── Farbe ermitteln ────────────────────────────────────────────────
    if args.color is not None:
        color_arg = args.color
    else:
        default_color = config.get("default_color", DEFAULT_CONFIG["default_color"])
        color_arg = " ".join(str(v) for v in default_color)

    try:
        rgb = parse_color(color_arg)
    except ValueError as exc:
        logger.error(exc)
        print(f"❌ {exc}")
        sys.exit(1)

    # ── Ausführen ──────────────────────────────────────────────────────
    manager = WLEDManager(ips)
    success = manager.set_all(rgb)

    # ── Speichern (falls -s) ───────────────────────────────────────────
    if args.save:
        save_config(ips, rgb)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""WLED Setter – steuert mehrere WLED-Geräte per HTTP JSON API.

Funktionen:

* **Effekt als Nummer** (= WLED-Effekt-ID), Liste im Hilfetext (``-h``).
* **Pro Gerät eigene Einstellungen** (Farbe, Effekt, Helligkeit).
* **Segmente**: ein Gerät in LED-Bereiche teilen, jeder Bereich mit eigenem
  Effekt (z. B. LED 0–29 statisch, LED 30–59 Rainbow).
* **Szenen-Wechsel** (``--loop``): mehrere Szenen pro Gerät, die im
  Intervall durchgeschaltet werden (z. B. statisch ↔ Rainbow).

Alles Detaillierte steht in der ``config.json``. CLI-Argumente ``-c``/``-e``
setzen dagegen schnell **alle** Geräte einheitlich.

Usage:
    python3 wled.py                      # config.json anwenden
    python3 wled.py --loop               # Szenen durchschalten
    python3 wled.py -e 9                 # alle Geräte: Rainbow
    python3 wled.py -c rot -e 0 -b 128   # alle Geräte: rot, statisch
    python3 wled.py -i 192.168.2.125 -e 2
    python3 wled.py -c blau -e 0 -s      # einheitlich anwenden + speichern
    python3 wled.py --list-effects
"""

import argparse
import json
import logging
import shutil
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

import requests

type RGB = list[int]
type Config = dict[str, Any]

# ---------------------------------------------------------------------------
# Pfade & Konstanten
# ---------------------------------------------------------------------------

CONFIG_FILE: Final[Path] = Path(__file__).parent / "config.json"
LOG_FILE: Final[Path] = Path(__file__).parent / "wled.log"

#: Farbnamen → RGB.
COLOR_NAME_MAP: Final[dict[str, RGB]] = {
    "rot":    [255,   0,   0],
    "grün":   [  0, 255,   0],
    "gruen":  [  0, 255,   0],
    "blau":   [  0,   0, 255],
    "orange": [255, 120,   0],
    "weiß":   [255, 255, 255],
    "weiss":  [255, 255, 255],
    "gelb":   [255, 255,   0],
}

VALID_COLOR_NAMES: Final[list[str]] = sorted(COLOR_NAME_MAP)

#: Effekt-ID → Name. Auswahl der gängigsten WLED-Effekte (IDs = WLED-intern).
#: Jede ID von 0–255 wird akzeptiert; die komplette, zur Firmware passende
#: Liste liefert ``--list-effects``.
EFFECTS: Final[dict[int, str]] = {
    0:  "Solid (statisch)",
    1:  "Blink",
    2:  "Breathe",
    3:  "Wipe",
    6:  "Sweep",
    8:  "Colorloop",
    9:  "Rainbow",
    10: "Scan",
    12: "Fade",
    13: "Theater",
    14: "Theater Rainbow",
    15: "Running",
    17: "Twinkle",
    20: "Sparkle",
    23: "Strobe",
    28: "Chase",
    38: "Aurora",
    41: "Lighthouse",
    42: "Fireworks",
    43: "Rain",
    45: "Fire Flicker",
    46: "Gradient",
    47: "Loading",
    49: "Fairy",
    63: "Pride 2015",
    64: "Juggle",
    65: "Palette",
    66: "Fire 2012",
    67: "Colorwaves",
    68: "Bpm",
}

#: Gültiger Bereich der WLED-Effekt-IDs.
EFFECT_ID_MIN: Final[int] = 0
EFFECT_ID_MAX: Final[int] = 255

DEFAULT_INTERVAL: Final[float] = 10.0
REQUEST_TIMEOUT: Final[int] = 5

#: Konfiguration, falls keine config.json existiert (Legacy-Format).
DEFAULT_CONFIG: Final[Config] = {
    "ips": ["192.168.2.169"],
    "default_color": [255, 0, 0],
    "default_effect": 0,
    "interval": DEFAULT_INTERVAL,
}

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Datenmodell
# ---------------------------------------------------------------------------


class ConfigError(ValueError):
    """Fehler in der Konfiguration oder in einer Farbangabe."""


@dataclass(frozen=True, slots=True)
class Segment:
    """LED-Bereich eines Geräts mit eigenem Effekt.

    Attributes:
        start (int): Erste LED (inklusive, ab 0).
        stop (int): Letzte LED (exklusive).
        color (RGB): Primärfarbe ``[R, G, B]``.
        effect (int): WLED-Effekt-ID.
    """

    start: int
    stop: int
    color: RGB
    effect: int


@dataclass(frozen=True, slots=True)
class Scene:
    """Ein Beleuchtungszustand eines Geräts.

    Ohne ``segments`` wird das ganze Band einheitlich gesetzt.

    Attributes:
        color (RGB): Primärfarbe ``[R, G, B]``.
        effect (int): WLED-Effekt-ID.
        brightness (int | None): Helligkeit 0–255 oder ``None`` (= global).
        segments (tuple[Segment, ...]): Optionale LED-Bereiche.
    """

    color: RGB
    effect: int
    brightness: int | None = None
    segments: tuple[Segment, ...] = ()


@dataclass(frozen=True, slots=True)
class Device:
    """Ein WLED-Gerät mit seinen Szenen.

    Attributes:
        ip (str): IP-Adresse (optional mit Port, z. B. ``"10.0.0.5:8080"``).
        scenes (tuple[Scene, ...]): Mind. eine Szene; mehrere für ``--loop``.
    """

    ip: str
    scenes: tuple[Scene, ...]


@dataclass(frozen=True, slots=True)
class Settings:
    """Vollständig geparste Konfiguration.

    Attributes:
        devices (tuple[Device, ...]): Alle konfigurierten Geräte.
        default_color (RGB): Standardfarbe.
        default_effect (int): Standardeffekt.
        interval (float): Sekunden zwischen Szenen im Loop-Modus.
    """

    devices: tuple[Device, ...]
    default_color: RGB
    default_effect: int
    interval: float


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


def setup_logging() -> None:
    """Richtet das Logging ein.

    Die Log-Datei erhält alles ab ``DEBUG``, das Terminal nur ``WARNING``
    und höher.
    """
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


# ---------------------------------------------------------------------------
# Farb- und Effekt-Parsing
# ---------------------------------------------------------------------------


def parse_color(color_arg: str) -> RGB:
    """Wandelt eine Farbangabe in RGB-Werte um.

    Unterstützte Formate:

    1. **Farbname**: z. B. ``"rot"`` (siehe ``COLOR_NAME_MAP``).
    2. **RGB**: Drei durch Leerzeichen getrennte Integer (0–255),
       z. B. ``"255 0 0"``.
    3. **Hex**: ``"#FF0000"``, ``"0xFF0000"``, ``"FF0000"`` oder die
       Kurzform ``"#F00"``.

    Args:
        color_arg (str): Farbangabe als String.

    Returns:
        RGB: Liste ``[R, G, B]`` mit Werten 0–255.

    Raises:
        ConfigError: Wenn die Angabe in keinem Format interpretiert werden
            kann.
    """
    text = color_arg.strip().lower()

    if text in COLOR_NAME_MAP:
        return list(COLOR_NAME_MAP[text])

    parts = text.split()
    if len(parts) == 3 and all(p.isdecimal() for p in parts):
        rgb = [int(p) for p in parts]
        if all(0 <= v <= 255 for v in rgb):
            return rgb

    hex_text = text.removeprefix("#").removeprefix("0x")
    if len(hex_text) in (3, 6) and all(c in "0123456789abcdef" for c in hex_text):
        if len(hex_text) == 3:
            hex_text = "".join(c * 2 for c in hex_text)
        return [int(hex_text[i:i + 2], 16) for i in (0, 2, 4)]

    raise ConfigError(
        f"Ungültige Farbangabe: '{color_arg}'. Erwartet: Farbname "
        f"({', '.join(VALID_COLOR_NAMES)}), drei RGB-Werte (0–255) "
        f"oder Hex (#RRGGBB, 0xRRGGBB, RRGGBB)."
    )


def parse_effect(value: str) -> int:
    """Wandelt eine Effekt-Angabe (Zahl) in eine gültige Effekt-ID um.

    Dient als ``type=`` für argparse.

    Args:
        value (str): Effekt-ID als String, z. B. ``"9"``.

    Returns:
        int: Effekt-ID im Bereich 0–255.

    Raises:
        argparse.ArgumentTypeError: Wenn der Wert keine Ganzzahl im
            Bereich 0–255 ist.
    """
    try:
        effect = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"'{value}' ist keine Zahl – siehe Effektliste im Hilfetext."
        ) from None

    if not EFFECT_ID_MIN <= effect <= EFFECT_ID_MAX:
        raise argparse.ArgumentTypeError(
            f"Effekt-ID {effect} außerhalb {EFFECT_ID_MIN}–{EFFECT_ID_MAX}."
        )
    return effect


def describe_effect(effect: int) -> str:
    """Gibt einen lesbaren Namen für eine Effekt-ID zurück.

    Args:
        effect (int): WLED-Effekt-ID.

    Returns:
        str: Name aus ``EFFECTS`` oder ``"Effekt <id>"`` für unbekannte IDs.
    """
    return EFFECTS.get(effect, f"Effekt {effect}")


def build_effect_help() -> str:
    """Baut die Effekt-Tabelle für den Hilfetext.

    Returns:
        str: Mehrzeiliger Text, eine Zeile pro Effekt (``ID  Name``).
    """
    lines = ["Effekte (-e <Nummer>):"]
    lines.extend(f"  {eid:>3}  {name}" for eid, name in EFFECTS.items())
    lines.append("")
    lines.append("Weitere IDs (0–255) funktionieren ebenfalls;")
    lines.append("komplette Liste deines Geräts: --list-effects")
    lines.append("Hinweis: Rainbow-Effekte ignorieren die Farbe (-c).")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Konfiguration: JSON → Datenmodell
# ---------------------------------------------------------------------------


def _as_int(value: Any, where: str, low: int, high: int) -> int:
    """Prüft, ob ein JSON-Wert eine Ganzzahl im Bereich ``low``–``high`` ist.

    Args:
        value (Any): Zu prüfender Wert.
        where (str): Fundstelle für Fehlermeldungen, z. B. ``"devices[0].effect"``.
        low (int): Untere Grenze (inklusive).
        high (int): Obere Grenze (inklusive).

    Returns:
        int: Der geprüfte Wert.

    Raises:
        ConfigError: Bei falschem Typ oder Bereich.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise ConfigError(f"{where}: Ganzzahl erwartet, erhalten: {value!r}")
    if not low <= value <= high:
        raise ConfigError(f"{where}: {value} außerhalb {low}–{high}.")
    return value


def _as_color(value: Any, where: str) -> RGB:
    """Wandelt einen JSON-Wert in eine RGB-Liste um.

    Args:
        value (Any): ``[R, G, B]`` oder ein String (Name/Hex/"R G B").
        where (str): Fundstelle für Fehlermeldungen.

    Returns:
        RGB: Liste ``[R, G, B]``.

    Raises:
        ConfigError: Bei ungültiger Farbangabe.
    """
    if isinstance(value, str):
        try:
            return parse_color(value)
        except ConfigError as exc:
            raise ConfigError(f"{where}: {exc}") from None
    if isinstance(value, list) and len(value) == 3:
        return [_as_int(v, f"{where}[{i}]", 0, 255) for i, v in enumerate(value)]
    raise ConfigError(f"{where}: Farbe als [R,G,B] oder String erwartet: {value!r}")


def _parse_scene(
    raw: Config,
    where: str,
    default_color: RGB,
    default_effect: int,
) -> Scene:
    """Parst eine Szene (oder ein Gerät mit Inline-Szene).

    Fehlende ``color``/``effect`` werden aus den Defaults ergänzt, bei
    Segmenten zuerst aus der Szene.

    Args:
        raw (Config): JSON-Objekt der Szene.
        where (str): Fundstelle für Fehlermeldungen.
        default_color (RGB): Fallback-Farbe.
        default_effect (int): Fallback-Effekt.

    Returns:
        Scene: Geparste Szene.

    Raises:
        ConfigError: Bei ungültigen Werten.
    """
    color = (
        _as_color(raw["color"], f"{where}.color")
        if "color" in raw else list(default_color)
    )
    effect = (
        _as_int(raw["effect"], f"{where}.effect", EFFECT_ID_MIN, EFFECT_ID_MAX)
        if "effect" in raw else default_effect
    )
    brightness = (
        _as_int(raw["brightness"], f"{where}.brightness", 0, 255)
        if "brightness" in raw else None
    )

    raw_segments = raw.get("segments", [])
    if not isinstance(raw_segments, list):
        raise ConfigError(f"{where}.segments: Liste erwartet.")

    segments: list[Segment] = []
    for idx, seg in enumerate(raw_segments):
        seg_where = f"{where}.segments[{idx}]"
        if not isinstance(seg, dict) or "start" not in seg or "stop" not in seg:
            raise ConfigError(f"{seg_where}: Objekt mit 'start' und 'stop' erwartet.")
        start = _as_int(seg["start"], f"{seg_where}.start", 0, 100_000)
        stop = _as_int(seg["stop"], f"{seg_where}.stop", 1, 100_000)
        if stop <= start:
            raise ConfigError(f"{seg_where}: 'stop' ({stop}) muss > 'start' ({start}) sein.")
        segments.append(
            Segment(
                start=start,
                stop=stop,
                color=_as_color(seg["color"], f"{seg_where}.color") if "color" in seg else color,
                effect=(
                    _as_int(seg["effect"], f"{seg_where}.effect", EFFECT_ID_MIN, EFFECT_ID_MAX)
                    if "effect" in seg else effect
                ),
            )
        )

    return Scene(color, effect, brightness, tuple(segments))


def parse_settings(raw: Config) -> Settings:
    """Wandelt das JSON-Dictionary in :class:`Settings` um.

    Unterstützt das neue Format (``devices``) und das alte
    (``ips`` + ``default_color`` + ``default_effect``).

    Args:
        raw (Config): Aus der JSON-Datei gelesenes Dictionary.

    Returns:
        Settings: Validierte Konfiguration.

    Raises:
        ConfigError: Bei ungültigem Aufbau oder Werten.
    """
    default_color = (
        _as_color(raw["default_color"], "default_color")
        if "default_color" in raw else list(DEFAULT_CONFIG["default_color"])
    )
    default_effect = (
        _as_int(raw["default_effect"], "default_effect", EFFECT_ID_MIN, EFFECT_ID_MAX)
        if "default_effect" in raw else DEFAULT_CONFIG["default_effect"]
    )
    interval = raw.get("interval", DEFAULT_INTERVAL)
    if isinstance(interval, bool) or not isinstance(interval, int | float) or interval <= 0:
        raise ConfigError(f"interval: Zahl > 0 erwartet, erhalten: {interval!r}")

    devices: list[Device] = []
    if "devices" in raw:
        raw_devices = raw["devices"]
        if not isinstance(raw_devices, list) or not raw_devices:
            raise ConfigError("devices: nicht-leere Liste erwartet.")
        for d_idx, dev in enumerate(raw_devices):
            where = f"devices[{d_idx}]"
            if not isinstance(dev, dict) or not isinstance(dev.get("ip"), str):
                raise ConfigError(f"{where}: Objekt mit String 'ip' erwartet.")
            raw_scenes = dev.get("scenes", [dev])
            if not isinstance(raw_scenes, list) or not raw_scenes:
                raise ConfigError(f"{where}.scenes: nicht-leere Liste erwartet.")
            scenes = tuple(
                _parse_scene(s, f"{where}.scenes[{s_idx}]", default_color, default_effect)
                for s_idx, s in enumerate(raw_scenes)
                if isinstance(s, dict)
            )
            if len(scenes) != len(raw_scenes):
                raise ConfigError(f"{where}.scenes: Einträge müssen Objekte sein.")
            devices.append(Device(dev["ip"].strip(), scenes))
    else:
        ips = raw.get("ips", DEFAULT_CONFIG["ips"])
        if not isinstance(ips, list) or not ips or not all(isinstance(i, str) for i in ips):
            raise ConfigError("ips: nicht-leere Liste von Strings erwartet.")
        scene = Scene(list(default_color), default_effect)
        devices = [Device(ip.strip(), (scene,)) for ip in ips]

    return Settings(tuple(devices), default_color, default_effect, float(interval))


def load_settings(config_path: Path = CONFIG_FILE) -> Settings:
    """Lädt die Konfiguration aus einer JSON-Datei.

    Existiert die Datei nicht, werden die Defaults verwendet. Eine
    **defekte** Datei ist ein Fehler (statt stillem Fallback), damit sich
    Tippfehler nicht unbemerkt auswirken.

    Args:
        config_path (Path): Pfad zur JSON-Konfigurationsdatei.

    Returns:
        Settings: Geparste Konfiguration.

    Raises:
        ConfigError: Bei unlesbarer oder ungültiger Datei.
    """
    if not config_path.exists():
        logger.warning(
            "Konfigurationsdatei '%s' nicht gefunden – verwende Defaults.",
            config_path,
        )
        return parse_settings(dict(DEFAULT_CONFIG))

    try:
        with open(config_path, encoding="utf-8") as fh:
            raw = json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        raise ConfigError(f"'{config_path}' nicht lesbar: {exc}") from exc

    if not isinstance(raw, dict):
        raise ConfigError(f"'{config_path}' muss ein JSON-Objekt enthalten.")

    logger.info("Konfiguration aus '%s' geladen.", config_path)
    return parse_settings(raw)


def save_settings(
    ips: list[str],
    color: RGB,
    effect: int,
    interval: float,
    config_path: Path = CONFIG_FILE,
) -> bool:
    """Speichert eine **einfache** Konfiguration (einheitlich, ohne Segmente).

    Eine bestehende Datei wird vorher als ``<name>.bak`` gesichert, weil
    Segmente und Szenen dabei verloren gehen.

    Args:
        ips (list[str]): IP-Adressen der Geräte.
        color (RGB): Standardfarbe ``[R, G, B]``.
        effect (int): Standard-Effekt-ID.
        interval (float): Sekunden zwischen Szenen im Loop-Modus.
        config_path (Path): Zielpfad der Konfigurationsdatei.

    Returns:
        bool: ``True`` bei Erfolg, ``False`` bei Schreibfehler.
    """
    config: Config = {
        "default_color": color,
        "default_effect": effect,
        "interval": interval,
        "devices": [{"ip": ip} for ip in ips],
    }
    try:
        if config_path.exists():
            shutil.copy2(config_path, config_path.with_suffix(".json.bak"))
        with open(config_path, "w", encoding="utf-8") as fh:
            json.dump(config, fh, indent=4, ensure_ascii=False)
            fh.write("\n")
    except OSError as exc:
        logger.error("Fehler beim Speichern der Konfiguration: %s", exc)
        print(f"❌ Fehler beim Speichern: {exc}")
        return False

    logger.info("Konfiguration gespeichert: %s", config)
    print(f"✅ Konfiguration nach {config_path} gespeichert (Backup: .json.bak).")
    return True


# ---------------------------------------------------------------------------
# Payload
# ---------------------------------------------------------------------------


def build_payload(
    scene: Scene,
    brightness: int,
    led_count: int | None,
    old_segment_count: int,
) -> dict[str, Any]:
    """Baut den JSON-State für eine Szene.

    Ohne Segmente wird Segment 0 über das ganze Band gelegt. Überzählige
    alte Segmente des Geräts werden gelöscht (``stop = 0``), damit sich
    Zustände nicht vermischen.

    Args:
        scene (Scene): Anzuwendende Szene.
        brightness (int): Helligkeit 0–255.
        led_count (int | None): LED-Anzahl des Geräts oder ``None``, wenn
            unbekannt.
        old_segment_count (int): Anzahl aktuell vorhandener Segmente.

    Returns:
        dict[str, Any]: Payload für ``POST /json/state``.
    """
    segs: list[dict[str, Any]]
    if scene.segments:
        segs = [
            {
                "id": i,
                "start": s.start,
                "stop": s.stop,
                "fx": s.effect,
                "col": [s.color],
                "on": True,
            }
            for i, s in enumerate(scene.segments)
        ]
    else:
        seg: dict[str, Any] = {
            "id": 0,
            "fx": scene.effect,
            "col": [scene.color],
            "on": True,
        }
        if led_count:
            seg["start"] = 0
            seg["stop"] = led_count
        segs = [seg]

    segs.extend({"id": i, "stop": 0} for i in range(len(segs), old_segment_count))
    return {"on": True, "bri": brightness, "seg": segs}


# ---------------------------------------------------------------------------
# WLED-Controller (ein Gerät)
# ---------------------------------------------------------------------------


class WLEDController:
    """Steuert ein einzelnes WLED-Gerät via HTTP JSON API.

    Attributes:
        ip (str): IP-Adresse des Geräts.
        state_url (str): URL des State-Endpunkts.
        info_url (str): URL des Info-Endpunkts.
        effects_url (str): URL der Effektnamen-Liste.
        timeout (int): Request-Timeout in Sekunden.
    """

    def __init__(self, ip: str, timeout: int = REQUEST_TIMEOUT) -> None:
        """Initialisiert den Controller.

        Args:
            ip (str): IP-Adresse, z. B. ``"192.168.2.169"``.
            timeout (int): Timeout für HTTP-Requests in Sekunden.
        """
        self.ip = ip
        self.state_url = f"http://{ip}/json/state"
        self.info_url = f"http://{ip}/json/info"
        self.effects_url = f"http://{ip}/json/eff"
        self.timeout = timeout

    def _get_json(self, url: str) -> Any | None:
        """Führt ein GET aus und liefert das geparste JSON.

        Args:
            url (str): Ziel-URL.

        Returns:
            Any | None: JSON-Inhalt oder ``None`` bei Fehler (Debug-Log).
        """
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.RequestException, ValueError) as exc:
            logger.debug("GET %s fehlgeschlagen: %s", url, exc)
            return None

    def get_state(self) -> dict[str, Any] | None:
        """Fragt den aktuellen Zustand des Geräts ab.

        Returns:
            dict[str, Any] | None: Zustand oder ``None`` bei Fehler.
        """
        return self._get_json(self.state_url)

    def get_info(self) -> dict[str, Any] | None:
        """Fragt die Geräte-Infos ab (u. a. LED-Anzahl).

        Returns:
            dict[str, Any] | None: Infos oder ``None`` bei Fehler.
        """
        return self._get_json(self.info_url)

    def get_effect_names(self) -> list[str] | None:
        """Fragt die Effektnamen des Geräts ab (Index = Effekt-ID).

        Returns:
            list[str] | None: Effektnamen oder ``None`` bei Fehler.
        """
        return self._get_json(self.effects_url)

    def apply_scene(self, scene: Scene, brightness: int = 255) -> bool:
        """Wendet eine Szene (Farbe, Effekt, ggf. Segmente) an.

        Args:
            scene (Scene): Anzuwendende Szene.
            brightness (int): Helligkeit 0–255 (Szene hat Vorrang).

        Returns:
            bool: ``True`` bei Erfolg, sonst ``False``.
        """
        info = self.get_info() or {}
        state = self.get_state() or {}
        led_count: int | None = info.get("leds", {}).get("count")
        old_segment_count = len(state.get("seg", []))

        if led_count:
            for seg in scene.segments:
                if seg.stop > led_count:
                    logger.warning(
                        "⚠️ %s → Segment %d–%d überschreitet LED-Anzahl (%d).",
                        self.ip, seg.start, seg.stop, led_count,
                    )

        bri = scene.brightness if scene.brightness is not None else brightness
        payload = build_payload(scene, bri, led_count, old_segment_count)

        try:
            response = requests.post(
                self.state_url, json=payload, timeout=self.timeout
            )
        except requests.exceptions.Timeout:
            logger.error("❌ %s → Timeout nach %s s.", self.ip, self.timeout)
            return False
        except requests.exceptions.ConnectionError as exc:
            logger.error("❌ %s → Verbindungsfehler: %s", self.ip, exc)
            return False
        except requests.exceptions.RequestException as exc:
            logger.error("❌ %s → Fehler: %s", self.ip, exc)
            return False

        if response.status_code != 200:
            logger.error(
                "❌ %s → HTTP %s – %s",
                self.ip,
                response.status_code,
                response.text.strip(),
            )
            return False

        if scene.segments:
            what = ", ".join(
                f"{s.start}-{s.stop}:{describe_effect(s.effect)}"
                for s in scene.segments
            )
        else:
            what = f"{scene.color}, {describe_effect(scene.effect)}"
        logger.info("✅ %s → %s (Helligkeit %s)", self.ip, what, bri)
        return True


# ---------------------------------------------------------------------------
# WLED-Manager (mehrere Geräte)
# ---------------------------------------------------------------------------


class WLEDManager:
    """Verwaltet mehrere Geräte mit je eigenen Szenen.

    Attributes:
        entries (list[tuple[WLEDController, Device]]): Controller + Konfig.
        brightness (int): Globale Helligkeit 0–255.
    """

    def __init__(self, devices: Sequence[Device], brightness: int = 255) -> None:
        """Erzeugt für jedes Gerät einen Controller.

        Args:
            devices (Sequence[Device]): Zu steuernde Geräte.
            brightness (int): Globale Helligkeit 0–255.
        """
        self.entries = [(WLEDController(d.ip), d) for d in devices]
        self.brightness = brightness
        logger.info(
            "Manager initialisiert mit %d Gerät(en): %s",
            len(self.entries),
            [d.ip for _, d in self.entries],
        )

    @property
    def has_multiple_scenes(self) -> bool:
        """bool: ``True``, wenn mindestens ein Gerät mehrere Szenen hat."""
        return any(len(d.scenes) > 1 for _, d in self.entries)

    def apply_step(self, step: int = 0) -> bool:
        """Wendet auf jedem Gerät die Szene ``step`` an (zyklisch).

        Args:
            step (int): Schrittzähler; Szene = ``scenes[step % len(scenes)]``.

        Returns:
            bool: ``True``, wenn **alle** Geräte erfolgreich waren.
        """
        results = [
            ctrl.apply_scene(dev.scenes[step % len(dev.scenes)], self.brightness)
            for ctrl, dev in self.entries
        ]
        failed = results.count(False)
        if failed:
            logger.warning(
                "⚠️ %d von %d Gerät(en) konnten nicht gesetzt werden.",
                failed,
                len(results),
            )
        return failed == 0

    def run_loop(self, interval: float) -> bool:
        """Schaltet die Szenen im Intervall durch, bis Strg+C gedrückt wird.

        Args:
            interval (float): Sekunden zwischen zwei Schritten.

        Returns:
            bool: ``True``, wenn bis zum Abbruch kein Gerät fehlgeschlagen ist.
        """
        step = 0
        all_ok = True
        print(f"🔁 Loop gestartet (alle {interval:g} s) – Abbruch mit Strg+C.")
        try:
            while True:
                all_ok &= self.apply_step(step)
                step += 1
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n⏹️ Loop beendet.")
        return all_ok


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

CONFIG_HELP: Final[str] = """\
Config-Beispiel (config.json):
  {
    "default_color": "blau", "default_effect": 0, "interval": 10,
    "devices": [
      {"ip": "192.168.2.169", "color": "rot", "effect": 9},
      {"ip": "192.168.2.125",
       "segments": [
         {"start": 0,  "stop": 30, "color": "blau", "effect": 0},
         {"start": 30, "stop": 60, "effect": 9}]},
      {"ip": "192.168.2.130",
       "scenes": [{"effect": 0, "color": "gelb"}, {"effect": 9}]}
    ]
  }
  - Ohne "color"/"effect" gelten die Defaults.
  - "scenes" werden mit --loop im Intervall durchgeschaltet.
  - Segmente: start inklusive, stop exklusive."""


def build_argument_parser() -> argparse.ArgumentParser:
    """Baut den ArgumentParser inklusive Effekt-Tabelle im Hilfetext.

    Returns:
        argparse.ArgumentParser: Fertig konfigurierter Parser.
    """
    parser = argparse.ArgumentParser(
        prog="wled.py",
        description=(
            "Steuert WLED-Geräte mit Farbe, Effekt, Segmenten und "
            "Szenen-Wechsel. Ohne Argumente wird die config.json angewendet; "
            "-c/-e überschreiben alle Geräte einheitlich."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            f"{build_effect_help()}\n\n"
            f"{CONFIG_HELP}\n\n"
            "Beispiele:\n"
            "  python3 wled.py\n"
            "  python3 wled.py --loop\n"
            "  python3 wled.py -e 9\n"
            '  python3 wled.py -c "255 120 0" -e 2 -b 128\n'
            "  python3 wled.py -i 192.168.2.125 -c blau -s\n"
            "  python3 wled.py --list-effects"
        ),
    )

    parser.add_argument(
        "-i", "--inventory",
        type=str,
        default=None,
        help=(
            'Komma-getrennte IP-Liste, z. B. "192.168.2.125,192.168.2.169". '
            "Bekannte IPs nutzen ihre config-Einstellungen."
        ),
    )
    parser.add_argument(
        "-c", "--color",
        type=str,
        default=None,
        help=(
            'Farbe für ALLE Geräte: Name, RGB ("255 0 0") oder Hex ("#FF0000"). '
            f"Namen: {', '.join(VALID_COLOR_NAMES)}."
        ),
    )
    parser.add_argument(
        "-e", "--effect",
        type=parse_effect,
        default=None,
        metavar="NR",
        help="Effekt-Nummer (0–255) für ALLE Geräte, Liste siehe unten.",
    )
    parser.add_argument(
        "-b", "--brightness",
        type=int,
        choices=range(0, 256),
        default=255,
        metavar="0-255",
        help="Globale Helligkeit (Default: 255; Szenen-Wert hat Vorrang).",
    )
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Szenen der Geräte im Intervall durchschalten (Abbruch: Strg+C).",
    )
    parser.add_argument(
        "-t", "--interval",
        type=float,
        default=None,
        metavar="SEK",
        help=f"Sekunden zwischen Szenen im Loop (Default: config, sonst {DEFAULT_INTERVAL:g}).",
    )
    parser.add_argument(
        "-s", "--save",
        action="store_true",
        help=(
            "Speichert IPs, Farbe und Effekt als EINFACHE config.json "
            "(Segmente/Szenen gehen verloren; Backup als .json.bak)."
        ),
    )
    parser.add_argument(
        "-l", "--list-effects",
        action="store_true",
        help="Listet alle Effekte des ersten Geräts (ID + Name) und beendet.",
    )
    return parser


def list_effects(ip: str) -> int:
    """Gibt alle Effekte eines Geräts auf der Konsole aus.

    Args:
        ip (str): IP-Adresse des Geräts.

    Returns:
        int: Exit-Code (0 = Erfolg, 1 = Gerät nicht erreichbar).
    """
    controller = WLEDController(ip)
    names = controller.get_effect_names()
    if names is None:
        print(f"❌ Effektliste von {controller.ip} nicht abrufbar.")
        return 1

    print(f"Effekte von {controller.ip}:")
    for effect_id, name in enumerate(names):
        print(f"  {effect_id:>3}  {name}")
    return 0


def resolve_devices(args: argparse.Namespace, settings: Settings) -> list[Device]:
    """Bestimmt die Geräte unter Berücksichtigung der CLI-Argumente.

    * ``-i`` wählt Geräte per IP; bekannte IPs behalten ihre Szenen,
      unbekannte erhalten die Defaults.
    * ``-c``/``-e`` ersetzen die Szenen **aller** Geräte durch eine
      einheitliche Szene (fehlender Wert → Default aus der Config).

    Args:
        args (argparse.Namespace): Geparste CLI-Argumente.
        settings (Settings): Geladene Konfiguration.

    Returns:
        list[Device]: Anzuwendende Geräte (kann bei leerem ``-i`` leer sein).

    Raises:
        ConfigError: Bei ungültiger Farbangabe ``-c``.
    """
    devices = list(settings.devices)

    if args.inventory is not None:
        known = {d.ip: d for d in devices}
        fallback = Scene(list(settings.default_color), settings.default_effect)
        ips = [ip.strip() for ip in args.inventory.split(",") if ip.strip()]
        devices = [known.get(ip) or Device(ip, (fallback,)) for ip in ips]

    if args.color is not None or args.effect is not None:
        color = parse_color(args.color) if args.color is not None else settings.default_color
        effect = args.effect if args.effect is not None else settings.default_effect
        uniform = Scene(color, effect)
        devices = [Device(d.ip, (uniform,)) for d in devices]

    return devices


def main(argv: Sequence[str] | None = None) -> int:
    """Hauptfunktion: CLI parsen, Konfiguration laden, Geräte setzen.

    Args:
        argv (Sequence[str] | None): Argumente ohne Programmname;
            ``None`` verwendet ``sys.argv``.

    Returns:
        int: Exit-Code (0 = alle Geräte OK, 1 = Fehler).
    """
    setup_logging()
    args = build_argument_parser().parse_args(argv)

    try:
        settings = load_settings()
        devices = resolve_devices(args, settings)
    except ConfigError as exc:
        logger.error(exc)
        print(f"❌ {exc}")
        return 1

    if not devices:
        logger.error("Keine gültigen IP-Adressen angegeben.")
        return 1

    if args.list_effects:
        return list_effects(devices[0].ip)

    interval = args.interval if args.interval is not None else settings.interval
    if interval <= 0:
        print("❌ Intervall muss > 0 sein.")
        return 1

    manager = WLEDManager(devices, args.brightness)

    if args.loop:
        if not manager.has_multiple_scenes:
            print("ℹ️ Kein Gerät hat mehrere 'scenes' – wende einmalig an.")
            success = manager.apply_step(0)
        else:
            success = manager.run_loop(interval)
    else:
        success = manager.apply_step(0)

    if args.save:
        if args.color is None and args.effect is None and args.inventory is None:
            print("ℹ️ -s speichert nur zusammen mit -c, -e oder -i – nichts gespeichert.")
        else:
            first = devices[0].scenes[0]
            save_settings([d.ip for d in devices], first.color, first.effect, interval)

    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
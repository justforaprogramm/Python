"""
main.py — CLI-Einstiegspunkt für das Zahlenraten-Spiel.

Unterstützte Zahlensysteme: Basis 2 (Binär) bis Basis 128.

Zeichenreihenfolge im Zahlenraum:
  0– 9  →  '0'–'9'
 10–35  →  'a'–'z'  (Kleinbuchstaben)
 36–61  →  'A'–'Z'  (Großbuchstaben)
 62–127 →  Sonderzeichen

Verwendung
----------
  python main.py                            # interaktives Menü
  python main.py --preset binary
  python main.py --preset hard
  python main.py --base 16 --min 1 --max 255 --attempts 8
  python main.py --base 36 --min 1 --max 1295
"""

import argparse
import sys

from config import GameConfig
from game import NumberGuessingGame
from numbase import ALPHABET, MAX_BASE, MIN_BASE, NumBase


# ------------------------------------------------------------------ #
# CLI-Hilfsklasse                                                      #
# ------------------------------------------------------------------ #

class CLI:
    """Statische Sammlung von Terminal-Ein-/Ausgabe-Hilfsmethoden."""

    BANNER = r"""
 ███╗   ██╗██╗   ██╗███╗   ███╗██████╗ ███████╗██████╗
 ████╗  ██║██║   ██║████╗ ████║██╔══██╗██╔════╝██╔══██╗
 ██╔██╗ ██║██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝
 ██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗
 ██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗██║  ██║
 ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
    Z A H L E N R A T E N   🎲   B a s i s   2 – 1 2 8
"""

    @staticmethod
    def print_banner() -> None:
        print(CLI.BANNER)

    @staticmethod
    def print_alphabet_info(base: int) -> None:
        """Zeigt den gültigen Zeichenvorrat für die aktuelle Basis."""
        chars = NumBase.digits_for(base)
        preview = chars if len(chars) <= 40 else chars[:40] + "…"
        print(f"  Gültige Zeichen für Basis {base}: {preview!r}")

    @staticmethod
    def prompt_base_string(
        prompt: str,
        lo: int,
        hi: int,
        base: int,
    ) -> str:
        """
        Fordert eine Eingabe in der angegebenen Basis an.
        Wiederholt bei ungültigen Zeichen oder Bereichsüberschreitung.

        Args:
            prompt: Anzeigetext.
            lo:     Untergrenze (Dezimal intern).
            hi:     Obergrenze (Dezimal intern).
            base:   Zahlenbasis.

        Returns:
            Gültige Eingabe als String (in der Basis).
        """
        lo_s = NumBase.encode(lo, base)
        hi_s = NumBase.encode(hi, base)
        while True:
            raw = input(prompt).strip()
            if raw.lower() in ("q", "quit", "exit", "beenden"):
                print("\nAuf Wiedersehen! 👋")
                sys.exit(0)
            try:
                value = NumBase.decode(raw, base)
            except ValueError as exc:
                print(f"  ⚠  Ungültige Eingabe: {exc}")
                continue
            if lo <= value <= hi:
                return raw
            print(
                f"  ⚠  Wert außerhalb des Bereichs "
                f"({lo_s}–{hi_s} in Basis {base}). Nochmal versuchen."
            )

    @staticmethod
    def prompt_int_plain(prompt: str, default: int) -> int:
        """Einfache Dezimaleingabe mit Standardwert (für Konfiguration)."""
        while True:
            raw = input(prompt).strip()
            if not raw:
                return default
            try:
                return int(raw)
            except ValueError:
                print("  ⚠  Bitte eine ganze Zahl eingeben.")

    @staticmethod
    def prompt_preset() -> str:
        """Fragt den Spieler nach dem gewünschten Spielmodus."""
        print("\nSpielmodus wählen:")
        print("  [1]  Easy     — Dezimal,      1–50,    12 Versuche, Hinweise AN")
        print("  [2]  Medium   — Dezimal,      1–100,   10 Versuche, Hinweise AN")
        print("  [3]  Hard     — Hexadezimal,  1–ff,     8 Versuche, Hinweise AUS")
        print("  [4]  Binary   — Binär (2),    1–11111, 10 Versuche, Hinweise AN")
        print("  [5]  Octal    — Oktal (8),    1–77,     9 Versuche, Hinweise AN")
        print("  [6]  Base36   — 0–9 + a–z,   1–zz,    10 Versuche, Hinweise AN")
        print("  [7]  Base62   — 0–9+a–z+A–Z, 1–ZZ,    10 Versuche, Hinweise AN")
        print("  [8]  Base128  — volles 128er, 1–~~~,   12 Versuche, Hinweise AN")
        print("  [9]  Eigene Basis / eigener Bereich")
        choice = input("\nEingabe (1–9): ").strip()
        mapping = {
            "1": "easy", "2": "medium", "3": "hard",
            "4": "binary", "5": "octal",
            "6": "base36", "7": "base62", "8": "base128",
            "9": "custom",
        }
        return mapping.get(choice, "medium")

    @staticmethod
    def build_custom_config() -> GameConfig:
        """Interaktiver Assistent für eine eigene Konfiguration."""
        print(f"\n── Eigene Konfiguration ──────────────────────────────")
        print(f"  Unterstützte Basen: {MIN_BASE}–{MAX_BASE}")
        print(f"  Zeichenreihenfolge: 0–9, a–z, A–Z, Sonderzeichen")

        base = CLI.prompt_int_plain(f"  Basis [{MIN_BASE}–{MAX_BASE}, Standard 10]: ", 10)
        try:
            NumBase.validate_base(base)
        except ValueError as exc:
            print(f"  ✗ {exc}  →  Setze Basis auf 10.")
            base = 10

        CLI.print_alphabet_info(base)

        min_n = CLI.prompt_int_plain("  Min (Dezimal) [Standard 1]: ", 1)
        max_n = CLI.prompt_int_plain("  Max (Dezimal) [Standard 100]: ", 100)
        attempts = CLI.prompt_int_plain("  Maximale Versuche [Standard 10]: ", 10)
        hints_raw = input("  Hinweise anzeigen? (j/n) [Standard j]: ").strip().lower()
        hints = hints_raw != "n"

        try:
            cfg = GameConfig(
                min_number=min_n,
                max_number=max_n,
                max_attempts=attempts,
                show_hints=hints,
                base=base,
            )
        except ValueError as exc:
            print(f"\n  ✗ Ungültige Konfiguration: {exc}")
            print("  Verwende Standardkonfiguration (Medium).\n")
            cfg = GameConfig.medium()

        # Zeige die Grenzen in der gewählten Basis
        print(
            f"\n  Konfiguration aktiv: {cfg}"
        )
        return cfg

    @staticmethod
    def ask_play_again() -> bool:
        return input("\nNochmal spielen? (j/n): ").strip().lower().startswith("j")


# ------------------------------------------------------------------ #
# Argument-Parser                                                      #
# ------------------------------------------------------------------ #

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Zahlenraten CLI — Basis 2 bis 128",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--preset",
        choices=["easy", "medium", "hard", "binary", "octal",
                 "base36", "base62", "base128"],
        help="Spiel direkt mit voreingestelltem Schwierigkeitsgrad starten.",
    )
    parser.add_argument(
        "--base", type=int, dest="base",
        help=f"Zahlenbasis ({MIN_BASE}–{MAX_BASE}), Standard 10.",
    )
    parser.add_argument("--min", type=int, dest="min_number",
                        help="Untergrenze (Dezimal), Standard 1.")
    parser.add_argument("--max", type=int, dest="max_number",
                        help="Obergrenze (Dezimal), Standard 100.")
    parser.add_argument("--attempts", type=int, dest="max_attempts",
                        help="Maximale Versuche, Standard 10.")
    parser.add_argument("--no-hints", action="store_true", dest="no_hints",
                        help="Heiß/Kalt-Hinweise deaktivieren.")
    return parser


def config_from_args(args: argparse.Namespace) -> GameConfig | None:
    """Gibt eine GameConfig aus CLI-Argumenten zurück oder None."""
    if args.preset:
        presets = {
            "easy": GameConfig.easy,
            "medium": GameConfig.medium,
            "hard": GameConfig.hard,
            "binary": GameConfig.binary,
            "octal": GameConfig.octal,
            "base36": GameConfig.base36,
            "base62": GameConfig.base62,
            "base128": GameConfig.base128,
        }
        return presets[args.preset]()

    if any([args.base, args.min_number, args.max_number, args.max_attempts]):
        try:
            return GameConfig(
                min_number=args.min_number or 1,
                max_number=args.max_number or 100,
                max_attempts=args.max_attempts or 10,
                show_hints=not args.no_hints,
                base=args.base or 10,
            )
        except ValueError as exc:
            print(f"Konfigurationsfehler: {exc}")
            sys.exit(1)

    return None


# ------------------------------------------------------------------ #
# Spielschleife                                                        #
# ------------------------------------------------------------------ #

def run_game(game: NumberGuessingGame) -> None:
    """Führt eine einzelne Spielrunde durch."""
    cfg = game.config
    lo_s = cfg.fmt(cfg.min_number)
    hi_s = cfg.fmt(cfg.max_number)

    print(f"\n{'─' * 55}")
    print(f"  {cfg}")
    print(f"  Rate eine Zahl zwischen {lo_s!r} und {hi_s!r}.")
    print(f"  Eingabe in {GameConfig.base_label(cfg.base)}.")
    print(f"  'q' zum Beenden.")
    print(f"{'─' * 55}\n")

    CLI.print_alphabet_info(cfg.base)
    print()

    while not game.is_over:
        attempt_num = game.attempts_used + 1
        prompt = f"  Versuch #{attempt_num}: "
        raw = CLI.prompt_base_string(
            prompt, cfg.min_number, cfg.max_number, cfg.base
        )
        try:
            feedback = game.make_guess(raw)
        except ValueError as exc:
            print(f"  ⚠  {exc}")
            continue

        print(f"\n  {feedback}")
        if not game.is_over:
            print(game.status_line())
        print()

    print(game.summary())


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    CLI.print_banner()

    config = config_from_args(args)

    while True:
        if config is None:
            preset = CLI.prompt_preset()
            if preset == "custom":
                active_config = CLI.build_custom_config()
            else:
                factory = {
                    "easy": GameConfig.easy,
                    "medium": GameConfig.medium,
                    "hard": GameConfig.hard,
                    "binary": GameConfig.binary,
                    "octal": GameConfig.octal,
                    "base36": GameConfig.base36,
                    "base62": GameConfig.base62,
                    "base128": GameConfig.base128,
                }[preset]
                active_config = factory()
        else:
            active_config = config

        game = NumberGuessingGame(active_config)
        run_game(game)

        if not CLI.ask_play_again():
            print("\nBis zum nächsten Mal! 👋\n")
            break

        config = None   # nach erster Runde immer neu abfragen


if __name__ == "__main__":
    main()
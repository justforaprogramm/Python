"""
main.py — CLI entry point for the Number Guessing Game.

Usage
-----
  python main.py                    # interactive setup
  python main.py --preset easy
  python main.py --min 1 --max 500 --attempts 8 --no-hints
"""

import argparse
import sys

from config import GameConfig
from game import NumberGuessingGame


# ------------------------------------------------------------------ #
# CLI helpers                                                          #
# ------------------------------------------------------------------ #

class CLI:
    """Static collection of terminal I/O helpers."""

    BANNER = r"""
 ███╗   ██╗██╗   ██╗███╗   ███╗██████╗ ███████╗██████╗
 ████╗  ██║██║   ██║████╗ ████║██╔══██╗██╔════╝██╔══██╗
 ██╔██╗ ██║██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝
 ██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗
 ██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗██║  ██║
 ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
          G U E S S I N G   G A M E  🎲
"""

    @staticmethod
    def print_banner() -> None:
        print(CLI.BANNER)

    @staticmethod
    def prompt_int(prompt: str, lo: int, hi: int) -> int:
        """Prompt until the user enters a valid integer in [lo, hi]."""
        while True:
            raw = input(prompt).strip()
            if raw.lower() in ("q", "quit", "exit"):
                print("\nThanks for playing. Goodbye! 👋")
                sys.exit(0)
            try:
                value = int(raw)
            except ValueError:
                print(f"  ⚠  Please enter a whole number between {lo} and {hi}.")
                continue
            if lo <= value <= hi:
                return value
            print(f"  ⚠  {value} is out of range ({lo}–{hi}). Try again.")

    @staticmethod
    def prompt_preset() -> str:
        """Ask the player to choose a difficulty preset."""
        print("\nChoose difficulty:")
        print("  [1] Easy    — range 1–50,  12 attempts, hints ON")
        print("  [2] Medium  — range 1–100, 10 attempts, hints ON")
        print("  [3] Hard    — range 1–200,  7 attempts, hints OFF")
        print("  [4] Custom  — configure your own settings")
        choice = input("\nEnter 1–4: ").strip()
        mapping = {"1": "easy", "2": "medium", "3": "hard", "4": "custom"}
        return mapping.get(choice, "medium")

    @staticmethod
    def build_custom_config() -> GameConfig:
        """Interactive wizard to build a custom GameConfig."""
        print("\n── Custom Configuration ──────────────────────────")
        min_n = int(input("  Min number [default 1]: ").strip() or "1")
        max_n = int(input("  Max number [default 100]: ").strip() or "100")
        attempts = int(input("  Max attempts [default 10]: ").strip() or "10")
        hints_raw = input("  Show hints? (y/n) [default y]: ").strip().lower()
        hints = hints_raw != "n"
        try:
            return GameConfig(
                min_number=min_n,
                max_number=max_n,
                max_attempts=attempts,
                show_hints=hints,
            )
        except ValueError as exc:
            print(f"\n  ✗ Invalid config: {exc}")
            print("  Falling back to medium difficulty.\n")
            return GameConfig.medium()

    @staticmethod
    def ask_play_again() -> bool:
        return input("\nPlay again? (y/n): ").strip().lower().startswith("y")


# ------------------------------------------------------------------ #
# Argument parsing                                                     #
# ------------------------------------------------------------------ #

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Number Guessing Game — CLI",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--preset",
        choices=["easy", "medium", "hard"],
        help="Start immediately with a named difficulty preset.",
    )
    parser.add_argument("--min", type=int, dest="min_number", help="Minimum number (default 1).")
    parser.add_argument("--max", type=int, dest="max_number", help="Maximum number (default 100).")
    parser.add_argument("--attempts", type=int, dest="max_attempts", help="Max attempts (default 10).")
    parser.add_argument(
        "--no-hints",
        action="store_true",
        dest="no_hints",
        help="Disable hot/cold hints.",
    )
    return parser


def config_from_args(args: argparse.Namespace) -> GameConfig | None:
    """Return a GameConfig if enough CLI args were supplied, else None."""
    if args.preset:
        presets = {"easy": GameConfig.easy, "medium": GameConfig.medium, "hard": GameConfig.hard}
        return presets[args.preset]()

    if any([args.min_number, args.max_number, args.max_attempts]):
        try:
            return GameConfig(
                min_number=args.min_number or 1,
                max_number=args.max_number or 100,
                max_attempts=args.max_attempts or 10,
                show_hints=not args.no_hints,
            )
        except ValueError as exc:
            print(f"Configuration error: {exc}")
            sys.exit(1)

    return None


# ------------------------------------------------------------------ #
# Main game loop                                                       #
# ------------------------------------------------------------------ #

def run_game(game: NumberGuessingGame) -> None:
    """Drive a single game round."""
    cfg = game.config
    print(f"\n{'─' * 50}")
    print(f"  Config  : {cfg}")
    print(f"  Guess a number between {cfg.min_number} and {cfg.max_number}.")
    print(f"  Type 'q' at any time to quit.")
    print(f"{'─' * 50}\n")

    while not game.is_over:
        attempt_num = game.attempts_used + 1
        prompt = f"  Guess #{attempt_num}: "
        guess = CLI.prompt_int(prompt, cfg.min_number, cfg.max_number)
        feedback = game.make_guess(guess)
        print(f"\n  {feedback}")
        if not game.is_over:
            print(game.status_line())
        print()

    print(game.summary())


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    CLI.print_banner()

    # Resolve config: CLI args → interactive wizard
    config = config_from_args(args)

    while True:
        if config is None:
            preset = CLI.prompt_preset()
            if preset == "custom":
                active_config = CLI.build_custom_config()
            else:
                active_config = {
                    "easy": GameConfig.easy,
                    "medium": GameConfig.medium,
                    "hard": GameConfig.hard,
                }[preset]()
        else:
            active_config = config

        game = NumberGuessingGame(active_config)
        run_game(game)

        if not CLI.ask_play_again():
            print("\nThanks for playing. See you next time! 👋\n")
            break

        # After first play, always re-prompt (ignore original CLI args)
        config = None


if __name__ == "__main__":
    main()
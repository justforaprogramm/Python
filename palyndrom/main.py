"""
palindrome – CLI palindrome checker
Usage:
    python3 main.py <string>
    python3 main.py <file.json>
    python3 main.py --help

    python3
    >>from main import Palindrome
    >>Palindrome.check(<string>)  # string out
    >>Palindrome.report(<string>) # json like

    pyinstaller --onefile main.py
    cd dist
    ./main <string>
    ./main <file.json>
    ./main --help
"""

# build CLI parsers and keep formatting in help/epilog text as-is
from argparse import ArgumentParser, RawDescriptionHelpFormatter

# serialize/deserialize JSON and catch parse errors
from json import dumps, loads, JSONDecodeError

# regex substitution, used to strip non-alphanumeric chars
from re import sub as resub

# exit the process with a status code
from sys import exit as sysexit

# object-oriented filesystem path handling
from pathlib import Path

# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------


class Palindrome:
    """Check whether a string is a palindrome or palindrome sentence."""

    @staticmethod
    def check(text: str) -> bool:
        """Return True if *text* is a palindrome (ignores spaces, punctuation, case)."""
        cleaned = resub(r"[^a-zA-Z0-9]", "", text).lower()
        return cleaned == cleaned[::-1]

    @staticmethod
    def report(text: str) -> dict:
        """Return a result dict for *text*."""
        result = Palindrome.check(text)
        return {"input": text, "is_palindrome": result}


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------


def load_strings_from_json(path: Path) -> list[str]:
    """Load a JSON file that contains a string or list of strings."""
    try:
        data = loads(path.read_text(encoding="utf-8"))
    except JSONDecodeError as exc:
        sysexit(f"Error: '{path}' is not valid JSON – {exc}")

    if isinstance(data, str):
        return [data]
    if isinstance(data, list) and all(isinstance(i, str) for i in data):
        return data
    sysexit(
        "Error: JSON file must contain a single string or an array of strings.\n"
        f"Got: {type(data).__name__}"
    )


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------


def print_results(results: list[dict]) -> None:
    """Pretty-print results to stdout."""
    width = max(len(r["input"]) for r in results) + 2
    for r in results:
        verdict = "✓ IS a palindrome" if r["is_palindrome"] else "✗ is NOT a palindrome"
        print(f'  {r["input"]!r:<{width}}  →  {verdict}')


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> ArgumentParser:
    """build and return the CLI argument parser with all arguments and help text"""
    parser = ArgumentParser(
        prog="main.py",
        description=(
            "Check whether one or more strings are palindromes.\n\n"
            "A palindrome reads the same forwards and backwards.\n"
            "Palindrome sentences ignore spaces, punctuation, and casing.\n\n"
            "Examples:\n"
            '  python3 main.py "racecar"\n'
            '  python3 main.py "A man a plan a canal Panama"\n'
            "  python3 main.py words.json"
        ),
        formatter_class=RawDescriptionHelpFormatter,
        epilog=(
            "JSON format\n"
            "-----------\n"
            '  A single string:      "racecar"\n'
            '  A list of strings:   ["racecar", "hello", "level"]\n\n'
            "Exit codes\n"
            "----------\n"
            "  0  All inputs are palindromes (or help/version shown)\n"
            "  1  At least one input is NOT a palindrome\n"
            "  2  Usage / file error\n"
        ),
    )
    parser.add_argument(
        "input",
        metavar="STR|FILE",
        help=(
            "A string to check, or the path to a .json file containing "
            "a string or list of strings."
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON instead of human-readable text.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="palindrome 1.0.0",
    )
    return parser


def main() -> None:
    """function to call only if the python file is called directly,
    manages that the pretty looks get called corretly
    """
    parser = build_parser()
    args = parser.parse_args()

    raw = args.input
    path = Path(raw)

    # file or string?
    if path.suffix.lower() == ".json" and path.exists():
        strings = load_strings_from_json(path)
    elif path.exists() and path.suffix.lower() != ".json":
        sysexit(f"Error: '{path}' exists but is not a .json file.")
    else:
        strings = [raw]

    results = [Palindrome.report(s) for s in strings]

    if args.json:
        print(dumps(results, ensure_ascii=False, indent=2))
    else:
        print()
        print_results(results)
        print()

    # Exit 1 if any input is not a palindrome
    if not all(r["is_palindrome"] for r in results):
        sysexit(1)


if __name__ == "__main__":
    main()

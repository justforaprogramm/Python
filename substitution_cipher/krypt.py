#!/usr/bin/env python3
"""
krypt.py - Ersetzt einzelne Buchstaben in einem Text durch andere.

Benutzung:
    python3 krypt.py n=b s=o "lmggs nsn,"

Jedes n=b bedeutet: jedes 'n' im Text wird zu 'b'.
Groß-/Kleinschreibung des Originalbuchstabens bleibt erhalten
(z.B. wird 'N' zu 'B', wenn n=b angegeben ist).
Der Text muss das letzte Argument sein (am besten in Anführungszeichen).
"""

import sys


def parse_args(args):
    mapping = {}
    text = None
    for arg in args:
        if text is None and "=" in arg:
            key, value = arg.split("=", 1)
            if len(key) == 1 and len(value) >= 1:
                mapping[key.lower()] = value
                continue
        text = arg
    return mapping, text


def substitute(text, mapping):
    result = []
    for char in text:
        lower = char.lower()
        if lower in mapping:
            replacement = mapping[lower]
            result.append(replacement.upper() if char.isupper() else replacement)
        else:
            result.append(char)
    return "".join(result)


def main():
    if len(sys.argv) < 2:
        print('Benutzung: python3 krypt.py n=b s=o "text"')
        sys.exit(1)

    mapping, text = parse_args(sys.argv[1:])

    if text is None:
        print("Fehler: Kein Text angegeben.")
        sys.exit(1)

    if not mapping:
        print("Fehler: Keine Ersetzungen (z.B. n=b) angegeben.")
        sys.exit(1)

    print(substitute(text, mapping))


if __name__ == "__main__":
    main()
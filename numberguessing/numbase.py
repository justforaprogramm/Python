"""
numbase.py — Basis-Konvertierung für das Zahlenraten-Spiel.

Unterstützt die Validierung sowie das Encoding und Decoding von Integern
in Zahlensysteme von Basis 2 bis Basis 128 unter Verwendung eines erweiterten
ASCII-Alphabets.
"""

import string

# 1. Aufbau des Alphabets nach deinen Vorgaben:
# 0–9  (10 Zeichen) -> '0'-'9'
# 10–35 (26 Zeichen) -> 'a'-'z'
# 36–61 (26 Zeichen) -> 'A'-'Z'
# 62–127 (66 Zeichen) -> Sichtbare ASCII-Sonderzeichen
_DIGITS = string.digits + string.ascii_lowercase + string.ascii_uppercase

# Wir füllen den Rest bis 128 mit sicheren ASCII-Sonderzeichen auf
_SPECIALS = "".join(
    chr(i)
    for i in range(32, 127)
    if chr(i) not in _DIGITS and chr(i) not in (" ", '"', "'", "\\")
)

ALPHABET = _DIGITS + _SPECIALS # pylint: disable=invalid-name

# Sicherheitscheck: Wir brauchen exakt 128 eindeutige Zeichen
if len(ALPHABET) < 128:
    FALLBACK = "".join(
        chr(i)
        for i in range(33, 255)
        if chr(i) not in ALPHABET and not chr(i).isspace()
    )
    ALPHABET += FALLBACK

ALPHABET = ALPHABET[:128] # pylint: disable=invalid-name

MIN_BASE = 2
MAX_BASE = 128


class NumBase:
    """Klasse zur Validierung und Konvertierung von Zahlen zwischen Basis 2 und 128."""

    @staticmethod
    def validate_base(base: int) -> None:
        """Prüft, ob die Basis im erlaubten Rahmen liegt."""
        if not MIN_BASE <= base <= MAX_BASE:
            raise ValueError(
                f"Die Basis muss zwischen {MIN_BASE} und {MAX_BASE} liegen (erhalten: {base})."
            )

    @staticmethod
    def digits_for(base: int) -> str:
        """Gibt den erlaubten Zeichenvorrat für eine bestimmte Basis zurück."""
        NumBase.validate_base(base)
        return ALPHABET[:base]

    @staticmethod
    def encode(number: int, base: int) -> str:
        """Konvertiert eine dezimale Ganzzahl (int) in einen String der Zielbasis."""
        NumBase.validate_base(base)

        if number == 0:
            return ALPHABET[0]

        is_negative = number < 0
        number = abs(number)

        result = []
        current_alphabet = ALPHABET[:base]

        while number > 0:
            number, remainder = divmod(number, base)
            result.append(current_alphabet[remainder])

        if is_negative:
            result.append("-")

        return "".join(reversed(result))

    @staticmethod
    def decode(encoded_str: str, base: int) -> int:
        """
        Konvertiert einen String einer Basis zurück in eine dezimale Ganzzahl.

        Wirft einen ValueError, wenn der String ungültige Zeichen enthält.
        """
        NumBase.validate_base(base)

        if not encoded_str:
            raise ValueError("Leere Eingabe ist nicht erlaubt.")

        current_alphabet = ALPHABET[:base]

        # Mapping von Zeichen zu ihrem Wert für schnellere Suche
        char_to_value = {char: idx for idx, char in enumerate(current_alphabet)}

        is_negative = False
        if encoded_str[0] == "-":
            is_negative = True
            encoded_str = encoded_str[1:]
            if not encoded_str:
                raise ValueError("Ungültiges Format (nur ein Minuszeichen).")

        result = 0
        for char in encoded_str:
            if char not in char_to_value:
                raise ValueError(
                    f"Das Zeichen {char!r} ist in Basis {base} nicht erlaubt."
                )
            result = result * base + char_to_value[char]

        return -result if is_negative else result

"""
config.py — Konfiguration für das Zahlenraten-Spiel.

Neu: ``base`` legt das Zahlensystem fest (2 = Binär … 128 = Base128).
Die Grenzen min_number/max_number werden intern als Dezimalwerte gespeichert;
die Darstellung gegenüber dem Spieler erfolgt in der gewählten Basis.
"""

from dataclasses import dataclass

from numbase import NumBase


@dataclass
class GameConfig:
    """Alle einstellbaren Parameter des Spiels."""

    min_number: int = 1
    max_number: int = 100
    max_attempts: int = 10
    show_hints: bool = True
    base: int = 10                  # Zahlensystem: 2–128

    # ------------------------------------------------------------------ #
    # Vorgefertigte Konfigurationen                                        #
    # ------------------------------------------------------------------ #

    @classmethod
    def easy(cls) -> "GameConfig":
        """Einfach: Dezimal, 1–50, 12 Versuche, Hinweise an."""
        return cls(min_number=1, max_number=50, max_attempts=12,
                   show_hints=True, base=10)

    @classmethod
    def medium(cls) -> "GameConfig":
        """Mittel: Dezimal, 1–100, 10 Versuche, Hinweise an."""
        return cls(min_number=1, max_number=100, max_attempts=10,
                   show_hints=True, base=10)

    @classmethod
    def hard(cls) -> "GameConfig":
        """Schwer: Hexadezimal, 1–255, 8 Versuche, Hinweise aus."""
        return cls(min_number=1, max_number=255, max_attempts=8,
                   show_hints=False, base=16)

    @classmethod
    def binary(cls) -> "GameConfig":
        """Binär-Modus: Basis 2, 1–31, 10 Versuche."""
        return cls(min_number=1, max_number=31, max_attempts=10,
                   show_hints=True, base=2)

    @classmethod
    def octal(cls) -> "GameConfig":
        """Oktal-Modus: Basis 8, 1–63, 9 Versuche."""
        return cls(min_number=1, max_number=63, max_attempts=9,
                   show_hints=True, base=8)

    @classmethod
    def base36(cls) -> "GameConfig":
        """Base36-Modus: 0–9 + a–z, 1–1295, 10 Versuche."""
        return cls(min_number=1, max_number=1295, max_attempts=10,
                   show_hints=True, base=36)

    @classmethod
    def base62(cls) -> "GameConfig":
        """Base62-Modus: 0–9 + a–z + A–Z, 1–3843, 10 Versuche."""
        return cls(min_number=1, max_number=3843, max_attempts=10,
                   show_hints=True, base=62)

    @classmethod
    def base128(cls) -> "GameConfig":
        """Base128-Modus: volles 128er-Alphabet, 1–16383, 12 Versuche."""
        return cls(min_number=1, max_number=16383, max_attempts=12,
                   show_hints=True, base=128)

    @classmethod
    def from_dict(cls, data: dict) -> "GameConfig":
        """Erstellt eine GameConfig aus einem Dictionary."""
        return cls(
            min_number=int(data.get("min_number", 1)),
            max_number=int(data.get("max_number", 100)),
            max_attempts=int(data.get("max_attempts", 10)),
            show_hints=bool(data.get("show_hints", True)),
            base=int(data.get("base", 10)),
        )

    # ------------------------------------------------------------------ #
    # Validierung                                                          #
    # ------------------------------------------------------------------ #

    @staticmethod
    def validate(
        min_number: int,
        max_number: int,
        max_attempts: int,
        base: int,
    ) -> None:
        """
        Wirft ValueError bei ungültigen Parametern.

        Args:
            min_number:   Untergrenze des Zahlenbereichs (Dezimal).
            max_number:   Obergrenze des Zahlenbereichs (Dezimal).
            max_attempts: Maximale Anzahl Rateversuche.
            base:         Zahlenbasis (2–128).

        Raises:
            ValueError: Bei logisch ungültigen Parametern.
        """
        if min_number >= max_number:
            raise ValueError(
                f"min_number ({min_number}) muss kleiner als "
                f"max_number ({max_number}) sein."
            )
        if max_attempts < 1:
            raise ValueError(
                f"max_attempts ({max_attempts}) muss mindestens 1 sein."
            )
        NumBase.validate_base(base)

    def __post_init__(self) -> None:
        GameConfig.validate(
            self.min_number, self.max_number, self.max_attempts, self.base
        )

    # ------------------------------------------------------------------ #
    # Anzeige-Hilfsmethoden                                                #
    # ------------------------------------------------------------------ #

    @staticmethod
    def base_label(base: int) -> str:
        """
        Gibt einen kurzen, lesbaren Namen für eine Basis zurück.

        Args:
            base: Zahlenbasis (2–128).

        Returns:
            Lesbarer Bezeichner, z. B. 'Binär (2)', 'Hexadezimal (16)'.
        """
        names = {
            2: "Binär", 3: "Ternär", 4: "Quaternär", 5: "Quinär",
            6: "Sextär", 7: "Septär", 8: "Oktal", 9: "Nonär",
            10: "Dezimal", 11: "Undezimal", 12: "Duodezimal",
            16: "Hexadezimal", 20: "Vigesimal", 32: "Base32",
            36: "Base36", 58: "Base58", 60: "Sexagesimal",
            62: "Base62", 64: "Base64*", 128: "Base128",
        }
        label = names.get(base, f"Basis {base}")
        return f"{label} ({base})"

    def fmt(self, value: int) -> str:
        """
        Formatiert einen Dezimalwert in der konfigurierten Basis.

        Args:
            value: Dezimalwert.

        Returns:
            String-Darstellung in self.base.
        """
        return NumBase.encode(value, self.base)

    def __str__(self) -> str:
        lo = self.fmt(self.min_number)
        hi = self.fmt(self.max_number)
        hints = "an" if self.show_hints else "aus"
        base_name = self.base_label(self.base)
        return (
            f"Zahlensystem: {base_name} | "
            f"Bereich [{lo}–{hi}] | "
            f"Versuche: {self.max_attempts} | Hinweise: {hints}"
        )
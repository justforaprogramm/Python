"""
config.py — Configuration for the Number Guessing Game.
"""

from dataclasses import dataclass, field


@dataclass
class GameConfig:
    """Holds all tunable parameters for the number guessing game."""

    min_number: int = 1
    max_number: int = 100
    max_attempts: int = 10
    show_hints: bool = True

    # ------------------------------------------------------------------ #
    # Class-level helpers                                                  #
    # ------------------------------------------------------------------ #

    @classmethod
    def easy(cls) -> "GameConfig":
        """Return a pre-built easy configuration (1–50, 12 attempts)."""
        return cls(min_number=1, max_number=50, max_attempts=12, show_hints=True)

    @classmethod
    def medium(cls) -> "GameConfig":
        """Return a pre-built medium configuration (1–100, 10 attempts)."""
        return cls(min_number=1, max_number=100, max_attempts=10, show_hints=True)

    @classmethod
    def hard(cls) -> "GameConfig":
        """Return a pre-built hard configuration (1–200, 7 attempts)."""
        return cls(min_number=1, max_number=200, max_attempts=7, show_hints=False)

    @classmethod
    def from_dict(cls, data: dict) -> "GameConfig":
        """Construct a GameConfig from a plain dictionary."""
        return cls(
            min_number=int(data.get("min_number", cls.min_number)),
            max_number=int(data.get("max_number", cls.max_number)),
            max_attempts=int(data.get("max_attempts", cls.max_attempts)),
            show_hints=bool(data.get("show_hints", cls.show_hints)),
        )

    # ------------------------------------------------------------------ #
    # Static helpers                                                       #
    # ------------------------------------------------------------------ #

    @staticmethod
    def validate(min_number: int, max_number: int, max_attempts: int) -> None:
        """
        Raise ValueError if the supplied parameters are logically invalid.

        Args:
            min_number:   Lower bound of the secret number range.
            max_number:   Upper bound of the secret number range.
            max_attempts: Maximum number of guesses allowed.

        Raises:
            ValueError: When any parameter violates a constraint.
        """
        if min_number >= max_number:
            raise ValueError(
                f"min_number ({min_number}) must be strictly less than "
                f"max_number ({max_number})."
            )
        if max_attempts < 1:
            raise ValueError(
                f"max_attempts ({max_attempts}) must be at least 1."
            )

    def __post_init__(self) -> None:
        GameConfig.validate(self.min_number, self.max_number, self.max_attempts)

    def __str__(self) -> str:
        hints = "on" if self.show_hints else "off"
        return (
            f"Range [{self.min_number}–{self.max_number}] | "
            f"Attempts: {self.max_attempts} | Hints: {hints}"
        )
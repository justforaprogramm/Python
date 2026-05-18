"""
game.py — Core logic for the Number Guessing Game.
"""

import random
from config import GameConfig


class NumberGuessingGame:
    """
    Encapsulates the state and logic of a single round.

    Attributes:
        config:        Active GameConfig instance.
        _secret:       The randomly chosen secret number.
        _attempts_left: Remaining guesses.
        _history:      Ordered list of previous guesses.
        _won:          Whether the player guessed correctly.
    """

    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self._secret: int = self._generate_secret(config.min_number, config.max_number)
        self._attempts_left: int = config.max_attempts
        self._history: list[int] = []
        self._won: bool = False

    # ------------------------------------------------------------------ #
    # Static helpers                                                       #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _generate_secret(min_number: int, max_number: int) -> int:
        """Return a random integer in [min_number, max_number] (inclusive)."""
        return random.randint(min_number, max_number)

    @staticmethod
    def _hint(guess: int, secret: int, show_hints: bool) -> str:
        """
        Build a directional hint string.

        Args:
            guess:      The player's guess.
            secret:     The secret number.
            show_hints: Whether temperature hints are enabled.

        Returns:
            A human-readable feedback string.
        """
        if guess == secret:
            return "🎯 Correct!"

        direction = "higher" if guess < secret else "lower"
        base = f"❌ Too {'low' if guess < secret else 'high'}! Go {direction}."

        if not show_hints:
            return base

        diff = abs(secret - guess)
        if diff <= 5:
            temperature = "🔥 Very hot"
        elif diff <= 15:
            temperature = "♨️  Hot"
        elif diff <= 30:
            temperature = "🌤  Warm"
        elif diff <= 50:
            temperature = "❄️  Cold"
        else:
            temperature = "🧊 Freezing"

        return f"{base} ({temperature})"

    @staticmethod
    def _ordinal(n: int) -> str:
        """Return the ordinal string for a positive integer (1 → '1st', etc.)."""
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10 if n % 100 not in (11, 12, 13) else 0, "th")
        return f"{n}{suffix}"

    # ------------------------------------------------------------------ #
    # Class-level factory                                                  #
    # ------------------------------------------------------------------ #

    @classmethod
    def from_preset(cls, preset: str) -> "NumberGuessingGame":
        """
        Create a game from a named preset ('easy', 'medium', 'hard').

        Args:
            preset: Difficulty name (case-insensitive).

        Returns:
            A fully initialised NumberGuessingGame.

        Raises:
            ValueError: When an unknown preset name is supplied.
        """
        presets = {
            "easy": GameConfig.easy,
            "medium": GameConfig.medium,
            "hard": GameConfig.hard,
        }
        key = preset.strip().lower()
        if key not in presets:
            raise ValueError(
                f"Unknown preset '{preset}'. Choose from: {', '.join(presets)}."
            )
        return cls(presets[key]())

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    @property
    def is_over(self) -> bool:
        """True when the game has ended (won or out of attempts)."""
        return self._won or self._attempts_left == 0

    @property
    def won(self) -> bool:
        """True if the player guessed the secret number."""
        return self._won

    @property
    def attempts_used(self) -> int:
        """Number of guesses made so far."""
        return self.config.max_attempts - self._attempts_left

    def make_guess(self, guess: int) -> str:
        """
        Process a single guess and return feedback.

        Args:
            guess: The player's integer guess.

        Returns:
            A feedback string.

        Raises:
            ValueError: If the guess is outside the valid range.
            RuntimeError: If the game is already over.
        """
        if self.is_over:
            raise RuntimeError("The game is already over.")

        lo, hi = self.config.min_number, self.config.max_number
        if not (lo <= guess <= hi):
            raise ValueError(f"Guess must be between {lo} and {hi}.")

        self._history.append(guess)
        self._attempts_left -= 1

        feedback = self._hint(guess, self._secret, self.config.show_hints)

        if guess == self._secret:
            self._won = True

        return feedback

    def status_line(self) -> str:
        """Return a concise status string for display after each guess."""
        remaining = self._attempts_left
        label = "attempt" if remaining == 1 else "attempts"
        return f"  ↳ {remaining} {label} remaining"

    def summary(self) -> str:
        """Return an end-of-game summary string."""
        if self._won:
            return (
                f"🏆 You won in {self._ordinal(self.attempts_used)} guess"
                f"{'es' if self.attempts_used != 1 else ''}! "
                f"The number was {self._secret}."
            )
        return f"💀 Game over! The secret number was {self._secret}."
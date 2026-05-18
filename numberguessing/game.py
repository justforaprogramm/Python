"""
game.py — Spiellogik für das Zahlenraten-Spiel.

Die geheime Zahl wird intern als Dezimalwert gespeichert.
Alle Ein- und Ausgaben erfolgen in der konfigurierten Basis.
"""

import random

from config import GameConfig
from numbase import NumBase


class NumberGuessingGame:
    """
    Kapselt Zustand und Logik einer einzelnen Spielrunde.

    Attributes:
        config:          Aktive GameConfig-Instanz.
        _secret:         Die zufällig gewählte Zahl (Dezimal intern).
        _attempts_left:  Verbleibende Rateversuche.
        _history:        Liste bisheriger Eingaben (als Strings in der Basis).
        _won:            Ob der Spieler richtig geraten hat.
    """

    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self._secret: int = self._generate_secret(
            config.min_number, config.max_number
        )
        self._attempts_left: int = config.max_attempts
        self._history: list[str] = []
        self._won: bool = False

    # ------------------------------------------------------------------ #
    # Statische Hilfsmethoden                                              #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _generate_secret(min_number: int, max_number: int) -> int:
        """
        Erzeugt einen zufälligen Integer in [min_number, max_number].

        Args:
            min_number: Untergrenze (inklusiv).
            max_number: Obergrenze (inklusiv).

        Returns:
            Zufälliger Dezimalwert.
        """
        return random.randint(min_number, max_number)

    @staticmethod
    def _hint(
        guess: int,
        secret: int,
        show_hints: bool,
        base: int,
    ) -> str:
        """
        Erstellt eine Rückmeldung für den gegebenen Ratewert.

        Args:
            guess:      Eingegebener Wert (Dezimal intern).
            secret:     Geheimzahl (Dezimal intern).
            show_hints: Ob Temperatur-Hinweise angezeigt werden.
            base:       Aktuelle Zahlenbasis (für Darstellung).

        Returns:
            Lesbare Feedback-Zeichenkette.
        """
        if guess == secret:
            return "🎯 Richtig!"

        direction = "größer" if guess < secret else "kleiner"
        base_repr = NumBase.encode(guess, base)
        base_secret = NumBase.encode(secret, base)
        _ = base_secret  # nur intern; wird im Spielfluss nicht verraten

        base_info = f" (Basis {base}: {base_repr!r})"
        base_text = f"❌ Zu {'klein' if guess < secret else 'groß'}! Gehe {direction}.{base_info}"

        if not show_hints:
            return base_text

        # Temperatur-Hinweis relativ zur Gesamtspanne
        diff = abs(secret - guess)
        if diff <= 2:
            temperature = "🔥 Sehr heiß"
        elif diff <= 8:
            temperature = "♨️  Heiß"
        elif diff <= 20:
            temperature = "🌤  Warm"
        elif diff <= 50:
            temperature = "❄️  Kalt"
        else:
            temperature = "🧊 Eiskalt"

        return f"{base_text} [{temperature}]"

    @staticmethod
    def _ordinal_de(n: int) -> str:
        """
        Gibt eine deutsche Ordinalzahl-Zeichenkette zurück.

        Args:
            n: Positive ganze Zahl.

        Returns:
            Z. B. '1.' für 1, '2.' für 2 usw.
        """
        return f"{n}."

    # ------------------------------------------------------------------ #
    # Klassenmethoden (Fabrikmethoden)                                     #
    # ------------------------------------------------------------------ #

    @classmethod
    def from_preset(cls, preset: str) -> "NumberGuessingGame":
        """
        Erstellt ein Spiel aus einem benannten Schwierigkeitsgrad.

        Args:
            preset: Name ('easy', 'medium', 'hard', 'binary', 'octal',
                    'base36', 'base62', 'base128').

        Returns:
            Fertig initialisiertes NumberGuessingGame.

        Raises:
            ValueError: Bei unbekanntem Preset-Namen.
        """
        presets: dict[str, object] = {
            "easy": GameConfig.easy,
            "medium": GameConfig.medium,
            "hard": GameConfig.hard,
            "binary": GameConfig.binary,
            "octal": GameConfig.octal,
            "base36": GameConfig.base36,
            "base62": GameConfig.base62,
            "base128": GameConfig.base128,
        }
        key = preset.strip().lower()
        if key not in presets:
            raise ValueError(
                f"Unbekanntes Preset '{preset}'. "
                f"Verfügbar: {', '.join(presets)}."
            )
        return cls(presets[key]())  # type: ignore[operator]

    # ------------------------------------------------------------------ #
    # Öffentliches Interface                                               #
    # ------------------------------------------------------------------ #

    @property
    def is_over(self) -> bool:
        """True wenn das Spiel beendet ist (gewonnen oder keine Versuche mehr)."""
        return self._won or self._attempts_left == 0

    @property
    def won(self) -> bool:
        """True wenn der Spieler die Zahl erraten hat."""
        return self._won

    @property
    def attempts_used(self) -> int:
        """Anzahl der bisher genutzten Rateversuche."""
        return self.config.max_attempts - self._attempts_left

    def make_guess(self, raw_input: str) -> str:
        """
        Verarbeitet eine Eingabe als String in der konfigurierten Basis
        und gibt Rückmeldung zurück.

        Args:
            raw_input: Eingabe des Spielers (z. B. '1010' für Binär).

        Returns:
            Feedback-String.

        Raises:
            ValueError: Bei ungültigem Zeichen oder Bereichsüberschreitung.
            RuntimeError: Wenn das Spiel bereits beendet ist.
        """
        if self.is_over:
            raise RuntimeError("Das Spiel ist bereits beendet.")

        cfg = self.config

        # Dekodieren
        try:
            guess = NumBase.decode(raw_input.strip(), cfg.base)
        except ValueError as exc:
            raise ValueError(str(exc)) from exc

        lo, hi = cfg.min_number, cfg.max_number
        if not (lo <= guess <= hi):
            lo_s = cfg.fmt(lo)
            hi_s = cfg.fmt(hi)
            raise ValueError(
                f"Eingabe muss zwischen {lo_s} und {hi_s} liegen "
                f"(Basis {cfg.base})."
            )

        self._history.append(raw_input.strip())
        self._attempts_left -= 1

        feedback = self._hint(guess, self._secret, cfg.show_hints, cfg.base)

        if guess == self._secret:
            self._won = True

        return feedback

    def status_line(self) -> str:
        """Gibt eine kurze Statuszeile nach jedem Rateversuch zurück."""
        remaining = self._attempts_left
        label = "Versuch" if remaining == 1 else "Versuche"
        return f"  ↳ Noch {remaining} {label} übrig"

    def summary(self) -> str:
        """Gibt eine Zusammenfassung am Spielende zurück."""
        secret_str = self.config.fmt(self._secret)
        if self._won:
            n = self.attempts_used
            return (
                f"🏆 Gewonnen nach {self._ordinal_de(n)} Versuch"
                f"{'en' if n != 1 else ''}! "
                f"Die gesuchte Zahl war {secret_str} "
                f"(Dezimal: {self._secret})."
            )
        return (
            f"💀 Spiel vorbei! Die gesuchte Zahl war {secret_str} "
            f"(Dezimal: {self._secret})."
        )
"""
deck.py – Kartenstapel-Verwaltung für das UNO-Spiel.

Enthält die Klassen Deck (Ziehstapel) und DiscardPile (Ablagestapel).
"""

import random
from typing import Optional

from cards import Card, CardType, Color


class Deck:
    """Verwaltet den Ziehstapel eines UNO-Spiels.

    Ein Standard-UNO-Deck hat 108 Karten:
    - 76 Zahlenkarten (je Farbe: eine 0, zwei 1–9)
    - 24 Aktionskarten (je Farbe: 2× Skip, 2× Reverse, 2× +2)
    - 8 Wild-Karten (4× Farbwechsel, 4× +4)

    Attributes:
        _cards (list[Card]): Die Karten im Ziehstapel.
    """

    def __init__(self) -> None:
        """Initialisiert und mischt einen vollständigen UNO-Kartensatz."""
        self._cards: list[Card] = []
        self._build()
        self.shuffle()

    # ------------------------------------------------------------------
    # Öffentliche Schnittstelle
    # ------------------------------------------------------------------

    def shuffle(self) -> None:
        """Mischt den Ziehstapel zufällig durch."""
        random.shuffle(self._cards)

    def draw(self) -> Optional[Card]:
        """Zieht die oberste Karte vom Ziehstapel.

        Returns:
            Die gezogene Karte, oder None wenn der Stapel leer ist.
        """
        if not self._cards:
            return None
        return self._cards.pop()

    def draw_many(self, count: int) -> list[Card]:
        """Zieht mehrere Karten vom Ziehstapel.

        Args:
            count: Anzahl der zu ziehenden Karten.

        Returns:
            Liste der gezogenen Karten (kann kürzer als count sein,
            wenn der Stapel erschöpft ist).
        """
        return [c for _ in range(count) if (c := self.draw()) is not None]

    def refill_from_discard(self, discard_pile: "DiscardPile") -> None:
        """Füllt den leeren Ziehstapel aus dem Ablagestapel auf.

        Die oberste Karte des Ablagestapels bleibt liegen; alle anderen
        Karten werden gemischt in den Ziehstapel überführt.

        Args:
            discard_pile: Der Ablagestapel, aus dem aufgefüllt wird.
        """
        recycled = discard_pile.recycle()
        for card in recycled:
            # Wild-Karten zurücksetzen
            if card.card_type in (CardType.WILD, CardType.WILD_DRAW_FOUR):
                card._chosen_color = None  # noqa: SLF001 – bewusster interner Reset
        self._cards = recycled
        self.shuffle()

    @property
    def remaining(self) -> int:
        """Gibt die Anzahl der verbliebenen Karten im Ziehstapel zurück."""
        return len(self._cards)

    def is_empty(self) -> bool:
        """Prüft, ob der Ziehstapel leer ist.

        Returns:
            True, wenn keine Karten mehr vorhanden sind.
        """
        return len(self._cards) == 0

    # ------------------------------------------------------------------
    # Interne Hilfsmethoden
    # ------------------------------------------------------------------

    def _build(self) -> None:
        """Baut einen vollständigen UNO-Kartensatz auf.

        Jede Nicht-Wild-Farbe erhält:
        - eine 0-Karte
        - je zwei Karten der Zahlen 1–9
        - je zwei Skip-, Reverse- und +2-Karten

        Zusätzlich werden vier Farbwechsel- und vier +4-Karten erzeugt.
        """
        normal_colors = [Color.RED, Color.GREEN, Color.YELLOW, Color.BLUE]

        for color in normal_colors:
            # Zahlenkarten
            self._cards.append(Card(color, CardType.NUMBER, 0))
            for num in range(1, 10):
                for _ in range(2):
                    self._cards.append(Card(color, CardType.NUMBER, num))

            # Aktionskarten (je 2×)
            for _ in range(2):
                self._cards.append(Card(color, CardType.SKIP))
                self._cards.append(Card(color, CardType.REVERSE))
                self._cards.append(Card(color, CardType.DRAW_TWO))

        # Wild-Karten
        for _ in range(4):
            self._cards.append(Card(Color.WILD, CardType.WILD))
            self._cards.append(Card(Color.WILD, CardType.WILD_DRAW_FOUR))

    def __len__(self) -> int:
        """Gibt die Anzahl der Karten im Ziehstapel zurück."""
        return len(self._cards)

    def __repr__(self) -> str:
        """Gibt eine Debug-Darstellung des Decks zurück."""
        return f"Deck({len(self._cards)} Karten verbleibend)"


class DiscardPile:
    """Verwaltet den Ablagestapel eines UNO-Spiels.

    Attributes:
        _cards (list[Card]): Die abgelegten Karten (letzte = oben).
    """

    def __init__(self) -> None:
        """Initialisiert einen leeren Ablagestapel."""
        self._cards: list[Card] = []

    # ------------------------------------------------------------------
    # Öffentliche Schnittstelle
    # ------------------------------------------------------------------

    def place(self, card: Card) -> None:
        """Legt eine Karte auf den Ablagestapel.

        Args:
            card: Die abzulegende Karte.
        """
        self._cards.append(card)

    @property
    def top(self) -> Optional[Card]:
        """Gibt die oberste Karte des Ablagestapels zurück, ohne sie zu entfernen.

        Returns:
            Die oberste Karte oder None, wenn der Stapel leer ist.
        """
        return self._cards[-1] if self._cards else None

    def recycle(self) -> list[Card]:
        """Entnimmt alle Karten außer der obersten zum Wiedereinmischen.

        Returns:
            Liste aller recycelten Karten.
        """
        if len(self._cards) <= 1:
            return []
        recycled = self._cards[:-1]
        self._cards = [self._cards[-1]]
        return recycled

    @property
    def size(self) -> int:
        """Gibt die Anzahl der Karten im Ablagestapel zurück."""
        return len(self._cards)

    def __repr__(self) -> str:
        """Gibt eine Debug-Darstellung des Ablagestapels zurück."""
        top = self._cards[-1] if self._cards else "leer"
        return f"DiscardPile(oben={top}, gesamt={len(self._cards)})"

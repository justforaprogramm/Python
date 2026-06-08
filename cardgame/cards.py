"""
cards.py – Karten-Modell für das UNO-Spiel.

Dieses Modul definiert alle Datenklassen und Enumerationen,
die eine UNO-Karte beschreiben.
"""

from enum import Enum, auto


class Color(Enum):
    """Enumeration der möglichen Kartenfarben."""

    RED = "Rot"
    GREEN = "Grün"
    YELLOW = "Gelb"
    BLUE = "Blau"
    WILD = "Wild"

    def __str__(self) -> str:
        """Gibt den deutschen Farbnamen zurück."""
        return self.value


class CardType(Enum):
    """Enumeration der möglichen Kartentypen."""

    NUMBER = auto()
    SKIP = auto()
    REVERSE = auto()
    DRAW_TWO = auto()
    WILD = auto()
    WILD_DRAW_FOUR = auto()

    def __str__(self) -> str:
        """Gibt eine lesbare Darstellung des Kartentyps zurück."""
        labels = {
            CardType.NUMBER: "Zahl",
            CardType.SKIP: "Aussetzen",
            CardType.REVERSE: "Richtungswechsel",
            CardType.DRAW_TWO: "+2",
            CardType.WILD: "Farbwechsel",
            CardType.WILD_DRAW_FOUR: "+4",
        }
        return labels[self]


class Card:
    """Repräsentiert eine einzelne UNO-Karte.

    Attributes:
        color (Color): Die Farbe der Karte.
        card_type (CardType): Der Typ der Karte.
        number (int | None): Die Zahl auf der Karte (nur bei Zahlenkarten).
        chosen_color (Color | None): Gewählte Farbe bei Wild-Karten nach dem Spielen.
    """

    def __init__(
        self,
        color: Color,
        card_type: CardType,
        number: int | None = None,
    ) -> None:
        """Initialisiert eine UNO-Karte.

        Args:
            color: Die Farbe der Karte.
            card_type: Der Typ der Karte.
            number: Die aufgedruckte Zahl (nur bei NUMBER-Karten relevant).

        Raises:
            ValueError: Wenn eine NUMBER-Karte keine gültige Zahl (0–9) hat.
            ValueError: Wenn eine Nicht-Wild-Karte die Farbe WILD erhält.
        """
        if card_type == CardType.NUMBER and number not in range(0, 10):
            raise ValueError(
                f"Zahlenkarten benötigen eine Zahl zwischen 0 und 9, erhalten: {number}"
            )
        if card_type not in (CardType.WILD, CardType.WILD_DRAW_FOUR) and color == Color.WILD:
            raise ValueError(
                "Nur Wild-Karten dürfen die Farbe WILD haben."
            )

        self._color = color
        self._card_type = card_type
        self._number = number
        self._chosen_color: Color | None = None

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def color(self) -> Color:
        """Gibt die Farbe der Karte zurück."""
        return self._color

    @property
    def card_type(self) -> CardType:
        """Gibt den Typ der Karte zurück."""
        return self._card_type

    @property
    def number(self) -> int | None:
        """Gibt die Zahl der Karte zurück, oder None wenn keine Zahlenkarte."""
        return self._number

    @property
    def chosen_color(self) -> Color | None:
        """Gibt die vom Spieler gewählte Farbe für Wild-Karten zurück."""
        return self._chosen_color

    @chosen_color.setter
    def chosen_color(self, color: Color) -> None:
        """Setzt die gewählte Farbe für eine Wild-Karte.

        Args:
            color: Die zu setzende Farbe. Darf nicht WILD sein.

        Raises:
            ValueError: Wenn die Karte keine Wild-Karte ist.
            ValueError: Wenn die Farbe WILD ist.
        """
        if self._card_type not in (CardType.WILD, CardType.WILD_DRAW_FOUR):
            raise ValueError("chosen_color kann nur bei Wild-Karten gesetzt werden.")
        if color == Color.WILD:
            raise ValueError("Die gewählte Farbe darf nicht WILD sein.")
        self._chosen_color = color

    @property
    def effective_color(self) -> Color:
        """Gibt die aktuell wirksame Farbe der Karte zurück.

        Bei Wild-Karten ist das die gewählte Farbe, sofern gesetzt,
        andernfalls WILD (Karte wurde noch nicht gespielt).

        Returns:
            Die wirksame Farbe dieser Karte.
        """
        if self._card_type in (CardType.WILD, CardType.WILD_DRAW_FOUR):
            return self._chosen_color if self._chosen_color else Color.WILD
        return self._color

    # ------------------------------------------------------------------
    # Vergleich & Spiellogik
    # ------------------------------------------------------------------

    def is_playable_on(self, top_card: "Card") -> bool:
        """Prüft, ob diese Karte auf die oberste Ablagestapelkarte gespielt werden darf.

        Eine Karte ist spielbar, wenn:
        - Sie eine Wild-Karte ist (immer spielbar), oder
        - ihre Farbe mit der wirksamen Farbe der Top-Karte übereinstimmt, oder
        - ihr Typ (bei Nicht-Zahlenkarten) mit dem Typ der Top-Karte übereinstimmt, oder
        - ihre Zahl mit der Zahl der Top-Karte übereinstimmt.

        Args:
            top_card: Die oberste Karte des Ablagestapels.

        Returns:
            True, wenn diese Karte gespielt werden darf.
        """
        if self._card_type in (CardType.WILD, CardType.WILD_DRAW_FOUR):
            return True
        effective_top = top_card.effective_color
        if self._color == effective_top:
            return True
        if self._card_type == top_card.card_type and self._card_type != CardType.NUMBER:
            return True
        if (
            self._card_type == CardType.NUMBER
            and top_card.card_type == CardType.NUMBER
            and self._number == top_card.number
        ):
            return True
        return False

    # ------------------------------------------------------------------
    # Darstellung
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """Gibt eine lesbare Darstellung der Karte zurück."""
        if self._card_type == CardType.NUMBER:
            return f"[{self._color}  {self._number}]"
        if self._card_type in (CardType.WILD, CardType.WILD_DRAW_FOUR):
            suffix = f"→{self._chosen_color}" if self._chosen_color else ""
            return f"[{self._card_type}{suffix}]"
        return f"[{self._color}  {self._card_type}]"

    def __repr__(self) -> str:
        """Gibt eine eindeutige Darstellung der Karte für Debug-Zwecke zurück."""
        return (
            f"Card(color={self._color!r}, type={self._card_type!r}, "
            f"number={self._number!r})"
        )

    def display_colored(self) -> str:
        """Gibt eine ANSI-farbige Darstellung der Karte zurück.

        Returns:
            String mit ANSI-Escape-Codes für farbige Terminal-Ausgabe.
        """
        ansi = {
            Color.RED: "\033[91m",
            Color.GREEN: "\033[92m",
            Color.YELLOW: "\033[93m",
            Color.BLUE: "\033[94m",
            Color.WILD: "\033[95m",
        }
        reset = "\033[0m"
        col = self.effective_color
        code = ansi.get(col, "")
        return f"{code}{self}{reset}"

"""
player.py – Spieler-Modell für das UNO-Spiel.

Dieses Modul enthält die Player-Klasse, die einen einzelnen UNO-Spieler
mitsamt seiner Hand und seinem UNO-Status repräsentiert.
"""

from cards import Card


class Player:
    """Repräsentiert einen UNO-Spieler.

    Attributes:
        _name (str): Der angezeigte Name des Spielers.
        _hand (list[Card]): Die Handkarten des Spielers.
        _said_uno (bool): Ob der Spieler in dieser Runde UNO gerufen hat.
        _wins (int): Anzahl der gewonnenen Runden.
    """

    def __init__(self, name: str) -> None:
        """Initialisiert einen neuen Spieler.

        Args:
            name: Der Name des Spielers. Darf nicht leer sein.

        Raises:
            ValueError: Wenn der Name leer oder nur aus Leerzeichen besteht.
        """
        self.name = name  # Nutzt den Property-Setter zur Validierung
        self._hand: list[Card] = []
        self._said_uno: bool = False
        self._wins: int = 0

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        """Gibt den Namen des Spielers zurück."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Setzt den Namen des Spielers.

        Args:
            value: Der neue Name. Muss mindestens ein Nicht-Leerzeichen enthalten.

        Raises:
            ValueError: Wenn der Name leer ist.
        """
        value = value.strip()
        if not value:
            raise ValueError("Der Spielername darf nicht leer sein.")
        self._name = value

    @property
    def hand(self) -> list[Card]:
        """Gibt eine Kopie der Handkarten zurück (schreibgeschützt)."""
        return list(self._hand)

    @property
    def hand_size(self) -> int:
        """Gibt die Anzahl der Handkarten zurück."""
        return len(self._hand)

    @property
    def said_uno(self) -> bool:
        """Gibt zurück, ob der Spieler UNO gerufen hat."""
        return self._said_uno

    @said_uno.setter
    def said_uno(self, value: bool) -> None:
        """Setzt den UNO-Status des Spielers.

        Args:
            value: True, wenn der Spieler UNO gerufen hat.
        """
        self._said_uno = value

    @property
    def wins(self) -> int:
        """Gibt die Anzahl der Siege des Spielers zurück."""
        return self._wins

    # ------------------------------------------------------------------
    # Hand-Management
    # ------------------------------------------------------------------

    def add_card(self, card: Card) -> None:
        """Fügt eine Karte zur Hand des Spielers hinzu.

        Args:
            card: Die hinzuzufügende Karte.
        """
        self._hand.append(card)
        # Wenn ein Spieler eine Karte bekommt, ist sein UNO-Ruf ungültig
        self._said_uno = False

    def add_cards(self, cards: list[Card]) -> None:
        """Fügt mehrere Karten zur Hand des Spielers hinzu.

        Args:
            cards: Die Liste der hinzuzufügenden Karten.
        """
        for card in cards:
            self._hand.append(card)
        if cards:
            self._said_uno = False

    def remove_card(self, index: int) -> Card:
        """Entfernt eine Karte aus der Hand und gibt sie zurück.

        Args:
            index: Der Index der zu entfernenden Karte (0-basiert).

        Returns:
            Die entfernte Karte.

        Raises:
            IndexError: Wenn der Index außerhalb des gültigen Bereichs liegt.
        """
        if not (0 <= index < len(self._hand)):
            raise IndexError(
                f"Ungültiger Kartenindex {index}. "
                f"Gültig: 0–{len(self._hand) - 1}."
            )
        return self._hand.pop(index)

    def get_playable_cards(self, top_card: Card) -> list[tuple[int, Card]]:
        """Gibt alle spielbaren Karten mit ihren Indizes zurück.

        Args:
            top_card: Die oberste Karte des Ablagestapels.

        Returns:
            Liste von (Index, Karte)-Tupeln der spielbaren Karten.
        """
        return [
            (i, card)
            for i, card in enumerate(self._hand)
            if card.is_playable_on(top_card)
        ]

    def has_playable_card(self, top_card: Card) -> bool:
        """Prüft, ob der Spieler mindestens eine spielbare Karte hat.

        Args:
            top_card: Die oberste Karte des Ablagestapels.

        Returns:
            True, wenn mindestens eine Karte gespielt werden kann.
        """
        return any(card.is_playable_on(top_card) for card in self._hand)

    def has_won(self) -> bool:
        """Prüft, ob der Spieler alle Handkarten abgelegt hat.

        Returns:
            True, wenn die Hand leer ist.
        """
        return len(self._hand) == 0

    def record_win(self) -> None:
        """Erhöht den Siegeszähler des Spielers um eins."""
        self._wins += 1

    def reset_uno_call(self) -> None:
        """Setzt den UNO-Status für eine neue Runde zurück."""
        self._said_uno = False

    def clear_hand(self) -> None:
        """Leert die Hand des Spielers (für Spielneubeginn)."""
        self._hand.clear()
        self._said_uno = False

    # ------------------------------------------------------------------
    # Darstellung
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """Gibt eine lesbare Darstellung des Spielers zurück."""
        return f"{self._name} ({self.hand_size} Karten)"

    def __repr__(self) -> str:
        """Gibt eine Debug-Darstellung des Spielers zurück."""
        return (
            f"Player(name={self._name!r}, "
            f"hand_size={self.hand_size}, "
            f"wins={self._wins})"
        )

    @classmethod
    def create(cls, player_number: int) -> "Player":
        """Erstellt einen neuen Spieler interaktiv per Nutzereingabe.

        Fragt nach dem Namen; bei leerer Eingabe wird ein Standardname
        ("Spieler N") verwendet.

        Args:
            player_number: Die Nummer des Spielers (für den Standardnamen).

        Returns:
            Eine neue Player-Instanz.
        """
        default = f"Spieler {player_number}"
        raw = input(
            f"  Name für Spieler {player_number} "
            f"(Enter für '{default}'): "
        ).strip()
        return cls(raw if raw else default)

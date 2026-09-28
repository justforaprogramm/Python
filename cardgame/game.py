"""game.py – Spiellogik-Engine für das UNO-Spiel."""

from cards import Card, CardType, Color
from deck import Deck, DiscardPile
from player import Player
import tui


class TurnDirection:
    """Verwaltet die Spielrichtung (Uhrzeigersinn oder gegen den Uhrzeigersinn)."""

    def __init__(self) -> None:
        """Initialisiert die Richtung standardmäßig im Uhrzeigersinn."""
        self._clockwise: bool = True

    @property
    def clockwise(self) -> bool:
        """Gibt den aktuellen Status der Spielrichtung zurück."""
        return self._clockwise

    @clockwise.setter
    def clockwise(self, value: bool) -> None:
        """Setzt den Status der Spielrichtung."""
        if not isinstance(value, bool):
            raise TypeError("Richtung muss ein boolescher Wert sein.")
        self._clockwise = value

    def reverse(self) -> None:
        """Invertiert die aktuelle Spielrichtung."""
        self.clockwise = not self.clockwise

    def next_index(self, current: int, total: int, skip: bool = False) -> int:
        """Berechnet den Index des nächsten Spielers basierend auf der Richtung.

        Args:
            current: Der Index des aktuellen Spielers.
            total: Die Gesamtzahl der aktiven Spieler.
            skip: Wenn True, wird der nächste Spieler übersprungen.
        """
        step = 1 if self.clockwise else -1
        nxt = (current + step) % total
        if skip:
            nxt = (nxt + step) % total
        return nxt

    def __str__(self) -> str:
        """Gibt eine visuelle Repräsentation der Richtung zurück."""
        return "→ Uhrzeigersinn" if self.clockwise else "← Gegen den Uhrzeigersinn"


class GameSettings:
    """Verwaltet die Konfigurationen und Einstellungen für das UNO-Spiel."""

    MIN_PLAYERS: int = 2
    MAX_PLAYERS: int = 8
    DEFAULT_HAND_SIZE: int = 7

    def __init__(self, player_count: int, stop_at_first_winner: bool = True, initial_hand_size: int = DEFAULT_HAND_SIZE) -> None:
        """Initialisiert die Spieleinstellungen mit Validierung.

        Raises:
            ValueError: Wenn die Spieleranzahl außerhalb des erlaubten Bereichs liegt.
        """
        self.player_count = player_count
        self.stop_at_first_winner = stop_at_first_winner
        self.initial_hand_size = initial_hand_size

    @property
    def player_count(self) -> int:
        """Gibt die konfigurierte Spieleranzahl zurück."""
        return self._player_count

    @player_count.setter
    def player_count(self, count: int) -> None:
        """Validiert und setzt die Spieleranzahl."""
        if not (self.MIN_PLAYERS <= count <= self.MAX_PLAYERS):
            raise ValueError(f"Spieleranzahl muss zwischen {self.MIN_PLAYERS} und {self.MAX_PLAYERS} liegen.")
        self._player_count = count

    @property
    def stop_at_first_winner(self) -> bool:
        """Gibt zurück, ob das Spiel beim ersten Gewinner endet."""
        return self._stop_at_first_winner

    @stop_at_first_winner.setter
    def stop_at_first_winner(self, stop: bool) -> None:
        """Setzt die Bedingung für das Spielende beim ersten Sieger."""
        if not isinstance(stop, bool):
            raise TypeError("stop_at_first_winner muss ein boolescher Wert sein.")
        self._stop_at_first_winner = stop

    @property
    def initial_hand_size(self) -> int:
        """Gibt die Anzahl der Startkarten pro Spieler zurück."""
        return self._initial_hand_size

    @initial_hand_size.setter
    def initial_hand_size(self, size: int) -> None:
        """Validiert und setzt die Anzahl der Startkarten."""
        if size <= 0:
            raise ValueError("Die Anzahl der Handkarten muss größer als 0 sein.")
        self._initial_hand_size = size

    @classmethod
    def from_input(cls) -> "GameSettings":
        """Erstellt eine GameSettings-Instanz über Benutzereingaben im TUI."""
        tui.print_banner()
        tui.print_separator("─", "Spielkonfiguration")
        print(f"\n  Wie viele Spieler? ({cls.MIN_PLAYERS}–{cls.MAX_PLAYERS})")
        count = tui.ask_int(f"  Spieleranzahl [{cls.MIN_PLAYERS}–{cls.MAX_PLAYERS}]: ", cls.MIN_PLAYERS, cls.MAX_PLAYERS)
        print()
        stop = tui.ask_yes_no("Nach dem ersten Gewinner aufhören?\n  (Nein = weiterspielen bis nur ein Spieler Karten hat)", default=True)
        return cls(player_count=count, stop_at_first_winner=stop)

    def __repr__(self) -> str:
        """Gibt eine Entwickler-Repräsentation der Einstellungen zurück."""
        return f"GameSettings(players={self.player_count}, stop_first={self.stop_at_first_winner}, hand={self.initial_hand_size})"


class Game:
    """Repräsentiert die Haupt-Engine des UNO-Spiels und steuert den Ablauf."""

    def __init__(self, settings: GameSettings, players: list[Player]) -> None:
        """Initialisiert das Spiel mit Einstellungen und einer Liste von Spielern.

        Raises:
            ValueError: Wenn die Anzahl der Spieler nicht mit den Settings übereinstimmt.
        """
        if len(players) != settings.player_count:
            raise ValueError(f"Erwartet {settings.player_count} Spieler, erhalten {len(players)}.")
        self._settings = settings
        self._players: list[Player] = list(players)
        self._deck = Deck()
        self._discard = DiscardPile()
        self._direction = TurnDirection()
        self.current_index = 0
        self._finished_players: list[Player] = []
        self.pending_draw = 0

    @property
    def current_index(self) -> int:
        """Gibt den Index des Spielers an, der gerade am Zug ist."""
        return self._current_index

    @current_index.setter
    def current_index(self, index: int) -> None:
        """Validiert und setzt den aktuellen Spieler-Index."""
        if not self._players and index == 0:
            self._current_index = 0
            return
        if not (0 <= index < len(self._players)):
            raise ValueError("Ungültiger Spieler-Index.")
        self._current_index = index

    @property
    def pending_draw(self) -> int:
        """Gibt die Anzahl der aufzusammelnden Strafkarten zurück."""
        return self._pending_draw

    @pending_draw.setter
    def pending_draw(self, count: int) -> None:
        """Setzt die Anzahl der aufzusammelnden Strafkarten."""
        if count < 0:
            raise ValueError("Strafkarten können nicht negativ sein.")
        self._pending_draw = count

    def setup(self) -> None:
        """Bereitet das Spiel vor: Karten werden gemischt, verteilt und die Startkarte aufgedeckt."""
        for player in self._players:
            player.clear_hand()
            for card in self._deck.draw_many(self._settings.initial_hand_size):
                player.add_card(card)

        while True:
            first = self._deck.draw()
            if first is None:
                raise RuntimeError("Kartenstapel leer beim Spielstart.")
            if first.card_type not in (CardType.WILD, CardType.WILD_DRAW_FOUR):
                self._discard.place(first)
                break
            self._deck._cards.insert(0, first)

        self._apply_initial_card_effect(self._discard.top)

    def run(self) -> list[Player]:
        """Startet die Spielschleife und läuft, bis die Endbedingung erfüllt ist."""
        self.setup()
        while not self._is_game_over():
            self._play_turn()
        return list(self._finished_players) + list(self._players)

    def _play_turn(self) -> None:
        """Führt einen einzelnen Spielzug für den aktuellen Spieler aus."""
        player = self._players[self.current_index]

        if self.pending_draw > 0:
            self._force_draw(player, self.pending_draw)
            self.pending_draw = 0
            self._advance_turn()
            return

        tui.clear_screen()
        tui.print_banner()
        tui.print_scoreboard(self._players)
        tui.print_top_card(self._discard.top)
        tui.print_player_turn_header(player.name, player.hand_size)

        playable = player.get_playable_cards(self._discard.top)
        tui.print_separator("─", f"{player.name}s Handkarten")
        self._print_hand_with_playability(player, playable)

        tui.print_action_menu(len(playable), self._deck.remaining, can_say_uno=True)

        card_played = False
        while not card_played:
            action = tui.get_player_action(playable)

            if action == "u":
                player.said_uno = True
                tui.print_success(f"{player.name} ruft UNO!")
                continue

            if action == "z":
                drawn = self._draw_card_for_player(player)
                if drawn and drawn.is_playable_on(self._discard.top):
                    tui.print_info(f"Gezogen: {tui.card_str(drawn)} – möchtest du sie direkt spielen?")
                    drawn_idx = player.hand_size - 1
                    drawn_playable = [(drawn_idx, drawn)]
                    tui.print_action_menu(1, self._deck.remaining, can_say_uno=True)
                    choice = tui.get_player_action(drawn_playable)
                    if choice == "u":
                        player.said_uno = True
                        tui.print_success(f"{player.name} ruft UNO!")
                        choice = tui.get_player_action(drawn_playable)
                    if choice == "1":
                        card = player.remove_card(drawn_idx)
                        self._play_card(player, card)
                        card_played = True
                        self._check_uno_penalty(player)
                        if player.has_won():
                            self._handle_winner(player)
                        return
                    else:
                        tui.print_info("Karte behalten – Zug endet.")
                        card_played = True
                else:
                    if drawn:
                        tui.print_info(f"Gezogen: {tui.card_str(drawn)} (nicht spielbar)")
                    else:
                        tui.print_warning("Ziehstapel leer – Ablagestapel wird gemischt.")
                    card_played = True
                self._advance_turn()
                return

            else:
                chosen_pos = int(action) - 1
                hand_index = playable[chosen_pos][0]
                card = player.remove_card(hand_index)
                self._play_card(player, card)
                card_played = True
                self._check_uno_penalty(player)
                if player.has_won():
                    self._handle_winner(player)
                return

    def _check_uno_penalty(self, player: Player) -> None:
        """Prüft, ob ein Spieler vergessen hat, UNO zu rufen, und bestraft ihn gegebenenfalls."""
        if player.hand_size == 1 and not player.said_uno:
            self._force_draw(player, 2)
            tui.print_warning(f"{player.name} hat UNO nicht gerufen – 2 Strafkarten!")
        elif player.hand_size != 1:
            player.said_uno = False

    def _handle_winner(self, player: Player) -> None:
        """Verarbeitet das Ausscheiden eines Spielers, der alle Karten abgelegt hat."""
        place = len(self._finished_players) + 1
        tui.print_winner(player.name, place)
        player.record_win()
        self._finished_players.append(player)
        self._players.pop(self.current_index)
        if self.current_index >= len(self._players):
            self.current_index = 0
        tui.press_enter()

    def _play_card(self, player: Player, card: Card) -> None:
        """Legt eine Karte auf den Ablagestapel und wendet bei Wild-Cards die Farbwahl an."""
        if card.card_type in (CardType.WILD, CardType.WILD_DRAW_FOUR):
            tui.print_separator("─", "Wild-Karte gespielt!")
            chosen = tui.choose_color()
            card.chosen_color = chosen
            tui.print_success(f"Farbe gewählt: {tui.color_str(chosen)}")

        self._discard.place(card)
        tui.print_info(f"{player.name} spielt {tui.card_str(card)}")
        self._apply_card_effect(card)

    def _apply_card_effect(self, card: Card) -> None:
        """Führt den Spezialeffekt einer gespielten Aktionskarte aus."""
        if card.card_type == CardType.REVERSE:
            self._direction.reverse()
            tui.print_info(f"Richtungswechsel! ({self._direction})")
            if len(self._players) == 2:
                self._advance_turn(skip=True)
                return

        elif card.card_type == CardType.SKIP:
            tui.print_info(
                f"{self._players[self._direction.next_index(self.current_index, len(self._players))].name}"
                " muss aussetzen!"
            )
            self._advance_turn(skip=True)
            return

        elif card.card_type == CardType.DRAW_TWO:
            self.pending_draw += 2
            next_p = self._players[self._direction.next_index(self.current_index, len(self._players))]
            tui.print_info(f"{next_p.name} muss {self.pending_draw} Karten ziehen!")

        elif card.card_type == CardType.WILD_DRAW_FOUR:
            self.pending_draw += 4
            next_p = self._players[self._direction.next_index(self.current_index, len(self._players))]
            tui.print_info(f"{next_p.name} muss {self.pending_draw} Karten ziehen!")

        self._advance_turn()

    def _apply_initial_card_effect(self, card: Card) -> None:
        """Wendet den Effekt der allerersten aufgedeckten Karte beim Spielstart an."""
        if card is None:
            return
        if card.card_type == CardType.REVERSE:
            self._direction.reverse()
        elif card.card_type == CardType.SKIP:
            self._advance_turn()
        elif card.card_type == CardType.DRAW_TWO:
            self.pending_draw = 2

    def _advance_turn(self, skip: bool = False) -> None:
        """Wechselt zum nächsten Spieler in der Zugreihenfolge."""
        if not self._players:
            return
        self.current_index = self._direction.next_index(
            self.current_index, len(self._players), skip=skip
        )

    def _draw_card_for_player(self, player: Player) -> Card | None:
        """Lässt einen Spieler eine Karte vom Deck ziehen und mischt falls nötig den Ablagestapel neu."""
        if self._deck.is_empty():
            self._deck.refill_from_discard(self._discard)
        card = self._deck.draw()
        if card:
            player.add_card(card)
        return card

    def _force_draw(self, player: Player, count: int) -> None:
        """Zwingt einen Spieler, eine bestimmte Anzahl von Karten zu ziehen."""
        for _ in range(count):
            self._draw_card_for_player(player)
        tui.print_warning(f"{player.name} zieht {count} Karte(n).")

    def _is_game_over(self) -> bool:
        """Prüft anhand der Einstellungen, ob die Bedingungen für das Spielende erreicht sind."""
        if self._settings.stop_at_first_winner:
            return len(self._finished_players) >= 1
        return len(self._players) <= 1

    def _print_hand_with_playability(self, player: Player, playable: list[tuple[int, Card]]) -> None:
        """Gibt die Handkarten des Spielers formatiert aus und markiert spielbare Karten."""
        playable_indices = {idx for idx, _ in playable}
        playable_map = {idx: pos + 1 for pos, (idx, _) in enumerate(playable)}
        _DIM = "\033[2m"
        _RESET = "\033[0m"
        _BOLD = "\033[1m"
        for i, card in enumerate(player.hand):
            if i in playable_indices:
                pos = playable_map[i]
                print(f"  {_BOLD}[{pos:2d}]{_RESET} {tui.card_str(card)}")
            else:
                print(f"  {_DIM} —  {tui.card_str(card)}{_RESET}")
        print()
"""
tui.py – Terminal-User-Interface-Helfer für das UNO-Spiel.

Dieses Modul stellt alle Ausgabe- und Eingabe-Funktionen bereit,
die für die TUI-Darstellung benötigt werden.
"""

import os
import shutil

from cards import Card, Color


# ── ANSI-Farbcodes ────────────────────────────────────────────────────────────
_ANSI = {
    Color.RED: "\033[91m",
    Color.GREEN: "\033[92m",
    Color.YELLOW: "\033[93m",
    Color.BLUE: "\033[94m",
    Color.WILD: "\033[95m",
}
_BOLD = "\033[1m"
_DIM = "\033[2m"
_RESET = "\033[0m"
_BG_DARK = "\033[40m"
_CYAN = "\033[96m"
_WHITE = "\033[97m"


def _term_width() -> int:
    """Gibt die aktuelle Terminalbreite zurück (Fallback: 80).

    Returns:
        Breite des Terminals in Zeichen.
    """
    return shutil.get_terminal_size((80, 24)).columns


def clear_screen() -> None:
    """Löscht den Terminalinhalt plattformübergreifend."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner() -> None:
    """Gibt das UNO-Titellogo im Terminal aus."""
    width = min(_term_width(), 60)
    border = "═" * width
    print(f"\n{_BOLD}{_CYAN}╔{border}╗{_RESET}")
    title = "🃏  U N O  –  Das Kartenspiel  🃏"
    pad = (width - len(title)) // 2
    print(f"{_BOLD}{_CYAN}║{' ' * pad}{title}{' ' * (width - pad - len(title))}║{_RESET}")
    print(f"{_BOLD}{_CYAN}╚{border}╝{_RESET}\n")


def print_separator(char: str = "─", label: str = "") -> None:
    """Gibt eine Trennlinie aus, optional mit einem zentrierten Label.

    Args:
        char: Das Zeichen, das für die Linie verwendet wird.
        label: Optionaler Text, der in die Linie eingebettet wird.
    """
    width = min(_term_width(), 72)
    if label:
        side = (width - len(label) - 2) // 2
        print(f"{_DIM}{char * side} {label} {char * side}{_RESET}")
    else:
        print(f"{_DIM}{char * width}{_RESET}")


def color_str(color: Color) -> str:
    """Gibt den Farbnamen farbig formatiert zurück.

    Args:
        color: Die zu formatende Farbe.

    Returns:
        ANSI-formatierter Farbstring.
    """
    code = _ANSI.get(color, "")
    return f"{_BOLD}{code}{color}{_RESET}"


def card_str(card: Card) -> str:
    """Gibt eine farbig formatierte Kartendarstellung zurück.

    Args:
        card: Die darzustellende Karte.

    Returns:
        ANSI-formatierter Kartenstring.
    """
    col = card.effective_color
    code = _ANSI.get(col, "")
    return f"{_BOLD}{code}{card}{_RESET}"


def print_top_card(card: Card) -> None:
    """Zeigt die oberste Ablagestapelkarte optisch hervorgehoben an.

    Args:
        card: Die oberste Karte des Ablagestapels.
    """
    print_separator("─", "Ablagestapel")
    print(f"  Oben liegt:  {card_str(card)}")
    print()


def print_hand(cards: list[Card], show_indices: bool = True) -> None:
    """Gibt die Handkarten eines Spielers nummeriert aus.

    Args:
        cards: Die auszugebenden Karten.
        show_indices: Wenn True, werden Indizes (1-basiert) vorangestellt.
    """
    if not cards:
        print(f"  {_DIM}(Keine Karten auf der Hand){_RESET}")
        return
    for i, card in enumerate(cards):
        idx = f"{_BOLD}[{i + 1:2d}]{_RESET} " if show_indices else "     "
        print(f"  {idx}{card_str(card)}")


def print_player_turn_header(player_name: str, hand_size: int) -> None:
    """Zeigt den Kopfbereich für einen Spielerzug an.

    Args:
        player_name: Name des aktiven Spielers.
        hand_size: Anzahl der Handkarten.
    """
    print_separator("═")
    print(
        f"\n  {_BOLD}{_WHITE}► {player_name} ist dran "
        f"({hand_size} Karte{'n' if hand_size != 1 else ''}){_RESET}\n"
    )


def print_scoreboard(players: list) -> None:
    """Gibt eine Übersicht aller Spieler mit Kartenanzahl aus.

    Args:
        players: Liste aller Player-Objekte.
    """
    print_separator("─", "Spielerübersicht")
    for player in players:
        bar = "▓" * player.hand_size + "░" * max(0, 14 - player.hand_size)
        uno_mark = f" {_BOLD}\033[91m★ UNO{_RESET}" if player.said_uno else ""
        print(
            f"  {_DIM}{player.name:<18}{_RESET}"
            f"  {_CYAN}{bar}{_RESET}"
            f"  {player.hand_size:2d}{uno_mark}"
        )
    print()


def print_action_menu(
    playable_count: int,
    deck_remaining: int,
    can_say_uno: bool,
) -> None:
    """Gibt das Aktionsmenü für den aktuellen Zug aus.

    Args:
        playable_count: Anzahl der spielbaren Karten.
        deck_remaining: Verbleibende Karten im Ziehstapel.
        can_say_uno: Ob die UNO-Option angezeigt werden soll.
    """
    print_separator("─", "Aktionen")
    if playable_count:
        print(
            f"  {_BOLD}[1–{playable_count}]{_RESET}"
            f"  Karte spielen ({playable_count} spielbar)"
        )
    print(f"  {_BOLD}[z]{_RESET}      Karte ziehen  ({deck_remaining} im Stapel)")
    print(f"  {_BOLD}[u]{_RESET}      UNO!")
    print()


def choose_color() -> Color:
    """Lässt den Spieler eine Farbe für eine Wild-Karte wählen.

    Wiederholt die Abfrage, bis eine gültige Eingabe erfolgt.

    Returns:
        Die gewählte Farbe (niemals Color.WILD).
    """
    colors = [Color.RED, Color.GREEN, Color.YELLOW, Color.BLUE]
    print_separator("─", "Farbwahl")
    for i, col in enumerate(colors, start=1):
        print(f"  {_BOLD}[{i}]{_RESET}  {color_str(col)}")
    while True:
        raw = input("\n  Farbe wählen [1–4]: ").strip()
        if raw in ("1", "2", "3", "4"):
            return colors[int(raw) - 1]
        print(f"  {_BOLD}\033[91mUngültige Eingabe – bitte 1 bis 4 eingeben.{_RESET}")


def get_player_action(
    playable_cards: list[tuple[int, Card]],
) -> str:
    """Liest eine Spieleraktion vom Terminal ein.

    Gültige Eingaben:
    - "z" → Karte ziehen
    - "u" → UNO rufen
    - Eine Zahl zwischen 1 und len(playable_cards) → Karte legen

    Args:
        playable_cards: Liste spielbarer (Index, Karte)-Tupel.

    Returns:
        Der normalisierte Eingabe-String ("z", "u" oder "1"…"N").
    """
    valid = {"z", "u"}
    valid.update(str(i) for i in range(1, len(playable_cards) + 1))
    while True:
        raw = input("  Aktion: ").strip().lower()
        if raw in valid:
            return raw
        print(
            f"  {_BOLD}\033[91mUngültige Eingabe. "
            f"Bitte wähle eine der angezeigten Optionen.{_RESET}"
        )


def ask_int(prompt: str, lo: int, hi: int) -> int:
    """Liest eine ganze Zahl im angegebenen Bereich ein.

    Args:
        prompt: Die Eingabeaufforderung.
        lo: Untere Grenze (inklusiv).
        hi: Obere Grenze (inklusiv).

    Returns:
        Die eingegebene Zahl.
    """
    while True:
        raw = input(prompt).strip()
        if raw.isdigit() and lo <= int(raw) <= hi:
            return int(raw)
        print(
            f"  {_BOLD}\033[91mBitte eine Zahl zwischen {lo} und {hi} eingeben.{_RESET}"
        )


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    """Stellt eine Ja/Nein-Frage und liest die Antwort ein.

    Args:
        prompt: Die Frage (ohne j/n-Hinweis, wird automatisch ergänzt).
        default: Standard-Antwort bei leerer Eingabe.

    Returns:
        True für Ja, False für Nein.
    """
    hint = "[J/n]" if default else "[j/N]"
    raw = input(f"  {prompt} {hint}: ").strip().lower()
    if raw == "":
        return default
    return raw in ("j", "ja", "y", "yes")


def print_info(message: str) -> None:
    """Gibt eine farbig hervorgehobene Info-Meldung aus.

    Args:
        message: Die auszugebende Nachricht.
    """
    print(f"  {_CYAN}ℹ  {message}{_RESET}")


def print_warning(message: str) -> None:
    """Gibt eine farbig hervorgehobene Warnmeldung aus.

    Args:
        message: Die auszugebende Nachricht.
    """
    print(f"  {_BOLD}\033[93m⚠  {message}{_RESET}")


def print_success(message: str) -> None:
    """Gibt eine grüne Erfolgsmeldung aus.

    Args:
        message: Die auszugebende Nachricht.
    """
    print(f"  {_BOLD}\033[92m✔  {message}{_RESET}")


def press_enter(prompt: str = "Enter drücken zum Weiterspielen…") -> None:
    """Pausiert und wartet auf eine Enter-Taste.

    Args:
        prompt: Die anzuzeigende Aufforderung.
    """
    input(f"\n  {_DIM}{prompt}{_RESET}")


def print_winner(player_name: str, place: int) -> None:
    """Gibt eine Gewinnermeldung für einen Spieler aus.

    Args:
        player_name: Name des Gewinners.
        place: Platzierung (1 = erster, 2 = zweiter, …).
    """
    suffix = {1: "🥇", 2: "🥈", 3: "🥉"}.get(place, "🏅")
    print(
        f"\n  {_BOLD}{_CYAN}{suffix}  {player_name} hat alle Karten abgelegt "
        f"– Platz {place}!{_RESET}\n"
    )


def print_final_scoreboard(ranked: list[tuple[int, str]]) -> None:
    """Gibt das Abschluss-Scoreboard nach Spielende aus.

    Args:
        ranked: Liste von (Platzierung, Spielername)-Tupeln in Reihenfolge.
    """
    print_separator("═", "Spielergebnis")
    for place, name in ranked:
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(place, "🏅")
        print(f"  {medal}  Platz {place}: {_BOLD}{name}{_RESET}")
    print()

"""
main.py – Einstiegspunkt für das UNO-Spiel.

Starte das Spiel einfach mit:
    python main.py
"""

from game import Game, GameSettings
from player import Player
import tui


def main() -> None:
    """Hauptschleife: Einstellungen → Spieler anlegen → Runde spielen → Wiederholen?"""
    while True:
        # 1) Konfiguration abfragen
        settings = GameSettings.from_input()

        # 2) Spieler anlegen
        tui.print_separator("─", "Spieler anlegen")
        print()
        players = [Player.create(i + 1) for i in range(settings.player_count)]

        # 3) Runde spielen
        game = Game(settings, players)
        ranking = game.run()

        # 4) Endergebnis anzeigen
        tui.clear_screen()
        tui.print_banner()
        tui.print_final_scoreboard([(i + 1, p.name) for i, p in enumerate(ranking)])

        # 5) Nochmal spielen?
        print()
        again = tui.ask_yes_no("Noch eine Runde spielen?", default=True)
        if not again:
            print("\n  Tschüss! 👋\n")
            break


if __name__ == "__main__":
    main()
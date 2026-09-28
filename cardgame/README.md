# 🃏 UNO – Das Kartenspiel

Ein vollständiges UNO-Spiel für das Terminal, geschrieben in Python 3.10+.  
Unterstützt 2–8 Spieler, farbige ANSI-Ausgabe und alle klassischen Sonderkarten.

---

## 🚀 Schnellstart

```bash
# Kein externes Paket nötig – nur Python 3.10+
python3 main.py
```

---

## 📁 Projektstruktur

```
uno/
├── main.py      # Einstiegspunkt – Spielschleife & Wiederholung
├── game.py      # Spiellogik-Engine (Züge, Effekte, Gewinner)
├── cards.py     # Datenmodell: Card, Color, CardType
├── deck.py      # Deck (Ziehstapel) & DiscardPile (Ablagestapel)
├── player.py    # Player-Klasse mit Hand-Management
└── tui.py       # Terminal-UI: Ausgaben, Eingaben, ANSI-Farben
```

---

## 🏗️ Architektur – Modulabhängigkeiten

```mermaid
graph TD
    main([main.py]) --> game
    main --> player
    main --> tui

    game([game.py]) --> cards
    game --> deck
    game --> player
    game --> tui

    deck([deck.py]) --> cards
    player([player.py]) --> cards

    tui([tui.py]) --> cards

    cards([cards.py])

    style main fill:#6366f1,color:#fff,stroke:none
    style game fill:#0ea5e9,color:#fff,stroke:none
    style deck fill:#10b981,color:#fff,stroke:none
    style player fill:#f59e0b,color:#fff,stroke:none
    style tui fill:#ec4899,color:#fff,stroke:none
    style cards fill:#64748b,color:#fff,stroke:none
```

---

## 🔄 Spielablauf

```mermaid
flowchart TD
    A([Spielstart]) --> B[Einstellungen abfragen\nSpieleranzahl, Spielmodus]
    B --> C[Spieler anlegen\nNamen eingeben]
    C --> D[Deck mischen\nKarten austeilen je 7]
    D --> E[Erste Karte aufdecken]
    E --> F{Aktionskarte\nals erste Karte?}
    F -- Reverse --> G[Richtung umkehren]
    F -- Skip --> H[Spieler 1 aussetzen]
    F -- +2 --> I[Spieler 1 zieht 2]
    F -- Nein --> J
    G & H & I --> J

    J([Zug beginnt]) --> K{Strafkarten\nausstehend?}
    K -- Ja --> L[Spieler zieht Strafkarten\nZug endet]
    K -- Nein --> M[Hand & spielbare Karten anzeigen]
    L --> N

    M --> O{Spieler-Aktion}
    O -- Karte spielen --> P[Karte auf Ablagestapel]
    O -- Karte ziehen --> Q[Karte vom Deck ziehen]
    O -- UNO rufen --> R[UNO-Flag setzen] --> O

    Q --> S{Gezogene Karte\nspielbar?}
    S -- Ja --> T{Direkt spielen?}
    S -- Nein --> N
    T -- Ja --> P
    T -- Nein --> N

    P --> U{Kartentyp?}
    U -- +2 / +4 --> V[pending_draw erhöhen]
    U -- Skip --> W[Nächsten Spieler überspringen]
    U -- Reverse --> X[Richtung umkehren]
    U -- Wild --> Y[Farbauswahl einholen]
    U -- Zahlenkarte --> N
    V & W & X & Y --> N

    N([UNO-Prüfung]) --> Z{1 Karte & kein UNO?}
    Z -- Ja --> AA[+2 Strafkarten]
    Z -- Nein --> AB

    AA --> AB{Hand leer?}
    AB -- Ja --> AC[Spieler gewinnt 🏆]
    AB -- Nein --> AD{Spielende?}
    AC --> AD

    AD -- Ja --> AE([Endergebnis anzeigen])
    AD -- Nein --> J
```

---

## 🃏 Kartenübersicht

```mermaid
classDiagram
    class Color {
        <<enumeration>>
        RED
        GREEN
        YELLOW
        BLUE
        WILD
    }

    class CardType {
        <<enumeration>>
        NUMBER
        SKIP
        REVERSE
        DRAW_TWO
        WILD
        WILD_DRAW_FOUR
    }

    class Card {
        +Color color
        +CardType card_type
        +int|None number
        +Color|None chosen_color
        +Color effective_color
        +is_playable_on(top_card) bool
        +display_colored() str
    }

    class Deck {
        -list~Card~ _cards
        +shuffle() None
        +draw() Card|None
        +draw_many(count) list~Card~
        +refill_from_discard(pile) None
        +remaining int
        +is_empty() bool
    }

    class DiscardPile {
        -list~Card~ _cards
        +place(card) None
        +top Card|None
        +recycle() list~Card~
        +size int
    }

    class Player {
        +str name
        -list~Card~ _hand
        -bool _said_uno
        -int _wins
        +add_card(card) None
        +remove_card(index) Card
        +get_playable_cards(top) list
        +has_won() bool
        +record_win() None
    }

    class Game {
        -GameSettings _settings
        -list~Player~ _players
        -Deck _deck
        -DiscardPile _discard
        -TurnDirection _direction
        -int _pending_draw
        +setup() None
        +run() list~Player~
    }

    Card --> Color
    Card --> CardType
    Deck "1" --> "0..*" Card
    DiscardPile "1" --> "0..*" Card
    Player "1" --> "0..*" Card
    Game "1" --> "1" Deck
    Game "1" --> "1" DiscardPile
    Game "1" --> "2..8" Player
```

---

## ⚙️ Spielregeln (Implementiert)

| Karte | Effekt |
|---|---|
| **Zahlenkarte** | Muss Farbe oder Zahl der obersten Karte treffen |
| **Skip** | Nächster Spieler setzt aus |
| **Reverse** | Spielrichtung dreht sich um (bei 2 Spielern = Skip) |
| **+2** | Nächster Spieler zieht 2 Karten und setzt aus |
| **Wild** | Spieler wählt eine neue Farbe |
| **+4** | Spieler wählt Farbe + Nächster zieht 4 Karten |
| **UNO vergessen** | +2 Strafkarten bei 1 Karte ohne UNO-Ruf |

---

## 🎮 Steuerung im Spiel

```
[1–N]   Spielbare Karte legen
[z]     Karte vom Stapel ziehen
[u]     UNO! rufen
[1–4]   Farbwahl bei Wild-Karten (Rot / Grün / Gelb / Blau)
```

---

## 🐍 Voraussetzungen

- Python **3.10** oder neuer (wegen `int | None` Union-Syntax)
- Keine externen Bibliotheken erforderlich
- Terminal mit ANSI-Farbunterstützung empfohlen (macOS, Linux, Windows Terminal)

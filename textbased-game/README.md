# textbased-game

## Projektbeschreibung
Dies ist ein textbasiertes Spiel, in dem der Spieler durch die Verwendung der Pfeiltasten auf einer Karte mit Wänden und Gegenständen navigieren kann. Der Spieler wird durch "#" dargestellt, Wände durch "I" und Gegenstände durch Symbole wie "+" oder "*".

## Dateien und Struktur
- **src/game.py**: Einstiegspunkt des Spiels mit der Hauptspielschleife und Eingabeverarbeitung.
- **src/map.py**: Definiert die Klasse `GameMap`, die die Spielkarte repräsentiert.
- **src/player.py**: Definiert die Klasse `Player`, die den Spieler repräsentiert.
- **src/utils.py**: Enthält Hilfsfunktionen für das Projekt.
- **tests/test_game.py**: Tests für die Spielmechanik.
- **tests/test_map.py**: Tests für die Kartenlogik.
- **tests/test_player.py**: Tests für die Bewegungslogik des Spielers.
- **requirements.txt**: Listet die Abhängigkeiten des Projekts auf.

## Installation
1. Klone das Repository oder lade die Dateien herunter.
2. Stelle sicher, dass Python 3.x installiert ist.
3. Installiere die Abhängigkeiten mit:
   ```
   pip install -r requirements.txt
   ```

## Ausführung
Um das Spiel zu starten, führe die folgende Datei aus:
```
python src/game.py
```

## Steuerung
- Verwende die Pfeiltasten, um dich auf der Karte zu bewegen.
- Interagiere mit Gegenständen, die auf der Karte platziert sind.

## Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert.
# 🎯 SudokuWPN — Stylisches Sudoku (Deutsch)

Ein kleines, grafisches Sudoku-Spiel in Python mit Pygame für das Spielbrett und Asciimatics für das Start-Menü. Minimalistisch, schnell und einfach anpassbar.

## ✨ Features
- Zufällig generierte, vollständige Sudoku-Boards ✅  
- Puzzle-Erstellung durch Entfernen von Feldern (Schwierigkeitsstufen) 🎚️  
- Start-Menü mit Schwierigkeit & Debug-Option (Asciimatics) 🎛️  
- Spiel-UI mit Pygame: Maus- und Tastatursteuerung 🖱️⌨️

## 🧩 Voraussetzungen
- Python 3.8+  
- pip  
- Empfohlene Bibliotheken:
  - pygame
  - asciimatics

## 🛠️ Installation (empfohlen virtuelles Environment)
```bash
# im Projektordner:
python -m venv .venv
# Windows aktivieren
.venv\Scripts\activate
# Abhängigkeiten installieren
pip install pygame asciimatics
```

## ▶️ Starten
Im Projektordner ausführen:
```bash
python main.py
```
Zuerst erscheint das Asciimatics-Setup-Menü (Schwierigkeit, Debug). Danach öffnet sich das Pygame-Fenster mit dem Spiel.

## 🎮 Steuerung
- Maus: Zelle auswählen  
- Zahlentasten 1–9: Zahl in ausgewählte Zelle eingeben (nur, wenn Slot frei)  
- Leertaste: Lösen / Cheat (abhängig vom Debug-Flag) ␣  
- R: Zurücksetzen ↩️  
- N: Neues Spiel ➕  
- Rücktaste / Entf: Eingabe löschen ⌫

## ⚙️ Konfiguration & wichtigste Konstanten
- DIFFICULTY: Anzahl der entfernten Felder (wird im Menü gesetzt)  
- DEBUG: Erlaubt Lösungs-Cheat (wird im Menü gesetzt)  
- BOARD_SIZE, CELL_SIZE, MARGIN, FPS — in main.py oben definiert

## 📂 Kurzer Code-Überblick
Hauptdatei: `main.py` — enthält:
- Board-Generator: `generate_full_board()`  
- Puzzle-Erzeugung: `generate_puzzle(board, blank_spaces)`  
- Validierung / Solver-Hilfen: `find_empty()`, `check_validity()`  
- Spielklasse: `Sudoku` (Spielzustand, Auswahl, Reset, New Game)  
- UI: `draw_board()` + `main()` (Event-Loop)  
- Setup-Menü: `run_sudoku_setup(screen)` (Asciimatics Frame)

## 🐞 Troubleshooting
- Schwarzes/weißes Fenster? Stelle sicher, dass pygame installiert ist und die Grafikkarte Treiber aktuell sind.  
- Reproduzierbare Puzzles: `random.seed(...)` vor Spielstart setzen.

Viel Spaß beim Spielen! 🎉
```// filepath: c:\Users\volls\Development\SudokuWPN\README.md
# 🎯 SudokuWPN — Stylisches Sudoku (Deutsch)

Ein kleines, grafisches Sudoku-Spiel in Python mit Pygame für das Spielbrett und Asciimatics für das Start-Menü. Minimalistisch, schnell und einfach anpassbar.

## ✨ Features
- Zufällig generierte, vollständige Sudoku-Boards ✅  
- Puzzle-Erstellung durch Entfernen von Feldern (Schwierigkeitsstufen) 🎚️  
- Start-Menü mit Schwierigkeit & Debug-Option (Asciimatics) 🎛️  
- Spiel-UI mit Pygame: Maus- und Tastatursteuerung 🖱️⌨️

## 🧩 Voraussetzungen
- Python 3.8+  
- pip  
- Empfohlene Bibliotheken:
  - pygame
  - asciimatics

## 🛠️ Installation (empfohlen virtuelles Environment)
```bash
# im Projektordner:
python -m venv .venv
# Windows aktivieren
.venv\Scripts\activate
# Abhängigkeiten installieren
pip install pygame asciimatics
```

## ▶️ Starten
Im Projektordner ausführen:
```bash
python main.py
```
Zuerst erscheint das Asciimatics-Setup-Menü (Schwierigkeit, Debug). Danach öffnet sich das Pygame-Fenster mit dem Spiel.

## 🎮 Steuerung
- Maus: Zelle auswählen  
- Zahlentasten 1–9: Zahl in ausgewählte Zelle eingeben (nur, wenn Slot frei)  
- Leertaste: Lösen / Cheat (abhängig vom Debug-Flag) ␣  
- R: Zurücksetzen ↩️  
- N: Neues Spiel ➕  
- Rücktaste / Entf: Eingabe löschen ⌫

## ⚙️ Konfiguration & wichtigste Konstanten
- DIFFICULTY: Anzahl der entfernten Felder (wird im Menü gesetzt)  
- DEBUG: Erlaubt Lösungs-Cheat (wird im Menü gesetzt)  
- BOARD_SIZE, CELL_SIZE, MARGIN, FPS — in main.py oben definiert

## 📂 Kurzer Code-Überblick
Hauptdatei: `main.py` — enthält:
- Board-Generator: `generate_full_board()`  
- Puzzle-Erzeugung: `generate_puzzle(board, blank_spaces)`  
- Validierung / Solver-Hilfen: `find_empty()`, `check_validity()`  
- Spielklasse: `Sudoku` (Spielzustand, Auswahl, Reset, New Game)  
- UI: `draw_board()` + `main()` (Event-Loop)  
- Setup-Menü: `run_sudoku_setup(screen)` (Asciimatics Frame)

## 🐞 Troubleshooting
- Schwarzes/weißes Fenster? Stelle sicher, dass pygame installiert ist und die Grafikkarte Treiber aktuell sind.  
- Reproduzierbare Puzzles: `random.seed(...)` vor Spielstart setzen.

Viel Spaß beim Spielen! 🎉
import pygame
import sys
import random
import time
from copy import deepcopy
from asciimatics.screen import Screen
from asciimatics.widgets import (
    Frame,
    Layout,
    Label,
    Button,
    CheckBox,
    PopUpDialog,
)
from asciimatics.scene import Scene
from asciimatics.exceptions import StopApplication

# Konstanten vor Initialisierung
WINDOW_SIZE = 1000
BOARD_SIZE = 900
CELL_SIZE = BOARD_SIZE // 9
MARGIN = (WINDOW_SIZE - BOARD_SIZE) // 2
FPS = 60
DEBUG = False
DIFFICULTY = 20

# Vorbestimmte Farben der Einfachheitshalber
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (50, 120, 200)
RED = (200, 50, 50)
GREEN = (50, 180, 80)
YELLOW = (240, 230, 140)


def find_empty(
    board,
):  # Überprüft, ob es leere Felder in dem Sudoku-Board gibt bzw gibt das erste leere Feld zurück
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0 or board[i][j] == "X":
                return i, j
    return None


def check_validity(
    board, row, column, target
):  # Überprüft, ob die in der Funktion angegebene Zahl (target) in der gegebenen Zeile, Spalte und 3x3 Box gültig ist
    for i in range(9):  # Schleife iteriert über Breite des Spielfelds
        if (
            board[row][i] == target or board[i][column] == target
        ):  # Überprüft Zeile und Spalte
            return False  # Falls ja, wird die Validität verletzt -> False zurückgeben

    box_row = (row // 3) * 3  # Berechnet Startposition der Box (Zeile)
    box_col = (column // 3) * 3  # Berechnet Startposition der Box (Spalte)
    for i in range(
        box_row, box_row + 3
    ):  # Äußere Schleife; iteriert durch die Zeile in der 3x3 Box
        for j in range(
            box_col, box_col + 3
        ):  # Innere Schleife; iteriert durch die Spalte in der 3x3 Box
            if (
                board[i][j] == target
            ):  # Überprüft jede Iteration, ob eine Koordinate in der Box dieselbe Zahl wie target ist
                return (
                    False  # Falls ja, wird die Validität verletzt -> False zurückgeben
                )

    return True  # Validität wurde über beide "Checkpoints" nicht verletzt -> True zurückgeben


def generate_full_board():
    board = [[0] * 9 for _ in range(9)]

    def fill_cell(index=0):
        if index == 81:
            return True
        row, column = divmod(index, 9)
        nums = list(range(1, 10))
        random.shuffle(nums)
        for num in nums:
            if check_validity(board, row, column, num):
                board[row][column] = num
                if fill_cell(index + 1):
                    return True
                board[row][column] = 0
        return False

    fill_cell()
    return board


def generate_puzzle(
    board, blank_spaces
):  # Generiert ein Sudoku-Rätsel mit einer bestimmten Anzahl an leeren Feldern
    while blank_spaces > 0:
        row = random.randint(0, 8)
        column = random.randint(0, 8)
        if board[row][column] != 0:
            board[row][column] = 0
            blank_spaces -= 1
    return board


class Sudoku:
    def __init__(self):
        self.full_board = generate_full_board()
        self.discarded_full_board = deepcopy(self.full_board)
        self.board = generate_puzzle(self.discarded_full_board, DIFFICULTY)
        self.original_board = deepcopy(self.board)
        self.selected = None
        self.cheat = False

    def select(self, pos):
        x, y = pos
        if (
            x < MARGIN
            or x >= MARGIN + BOARD_SIZE
            or y < MARGIN
            or y >= MARGIN + BOARD_SIZE
        ):
            self.selected = None
            return
        row = (y - MARGIN) // CELL_SIZE
        column = (x - MARGIN) // CELL_SIZE
        self.selected = (row, column)

    def clear_cell(self, row, column):
        if self.board[row][column] != 0:
            self.board[row][column] = 0
        return

    def reset(self):
        self.board = deepcopy(self.original_board)

    def new_game(self):
        self.full_board = generate_full_board()
        self.discarded_full_board = deepcopy(self.full_board)
        self.board = generate_puzzle(self.discarded_full_board, DIFFICULTY)
        self.original_board = deepcopy(self.board)
        self.selected = None
        self.cheat = False


def draw_board(sudoku):
    screen.fill(WHITE)
    for r in range(10):
        line_width = 4 if r % 3 == 0 else 1  # Dickere Linien für 3x3 Boxen
        pygame.draw.line(
            screen,
            BLACK,
            (MARGIN, MARGIN + r * CELL_SIZE),
            (MARGIN + BOARD_SIZE, MARGIN + r * CELL_SIZE),
            line_width,
        )  # Horizontale Linien
        pygame.draw.line(
            screen,
            BLACK,
            (MARGIN + r * CELL_SIZE, MARGIN),
            (MARGIN + r * CELL_SIZE, MARGIN + BOARD_SIZE),
            line_width,
        )  # Vertikale Linien

    for r in range(9):
        for c in range(9):
            num = sudoku.board[r][c]
            if num != 0:
                color = BLACK if num != "X" else RED
                text = FONT.render(str(num), True, color)
                screen.blit(
                    text,
                    (
                        MARGIN + c * CELL_SIZE + CELL_SIZE // 3,
                        MARGIN + r * CELL_SIZE + CELL_SIZE // 5,
                    ),
                )

    if sudoku.selected:
        r, c = sudoku.selected
        pygame.draw.rect(
            screen,
            YELLOW,
            (MARGIN + c * CELL_SIZE, MARGIN + r * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            3,
        )

    instruction_text = SMALL_FONT.render(
        "Leertaste: Lösen | R: Zurücksetzen | 1-9: Zahl | Rücktaste/Entf: Slot zurücksetzen | N: Neues Spiel",
        True,
        BLACK,
    )
    instruction_text_rect = instruction_text.get_rect(
        center=(WINDOW_SIZE // 2, WINDOW_SIZE - 30)
    )
    screen.blit(instruction_text, instruction_text_rect)

    pygame.display.flip()


def main():
    sudoku = Sudoku()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                sudoku.select(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sudoku.cheat = True
                    sudoku.board = deepcopy(sudoku.full_board)
                    if find_empty(sudoku.board) is None and (not sudoku.cheat or DEBUG):
                        for _ in range(3):
                            draw_board(sudoku)
                            pygame.display.flip()
                            time.sleep(0.5)
                            screen.fill(WHITE)
                            victory_text = FONT.render(
                                "Glückwunsch! Du hast das Sudoku gelöst!", True, GREEN
                            )
                            victory_text_rect = victory_text.get_rect(
                                center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2)
                            )
                            screen.blit(victory_text, victory_text_rect)
                            pygame.display.flip()
                            time.sleep(0.5)
                        draw_board(sudoku)
                        time.sleep(0.5)
                        screen.fill(WHITE)
                        intermission_text = FONT.render(
                            "Starte neues Spiel...", True, BLACK
                        )
                        intermission_text_rect = intermission_text.get_rect(
                            center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2)
                        )
                        screen.blit(intermission_text, intermission_text_rect)
                        pygame.display.flip()
                        time.sleep(2)
                        sudoku.new_game()
                if event.key == pygame.K_r:
                    sudoku.reset()
                if event.key == pygame.K_n:
                    sudoku.new_game()
                if sudoku.selected:
                    r, c = sudoku.selected
                    if sudoku.original_board[r][c] == 0:
                        # Mapping von Tastencode zu Zahl
                        key_to_num = {
                            pygame.K_1: 1,
                            pygame.K_2: 2,
                            pygame.K_3: 3,
                            pygame.K_4: 4,
                            pygame.K_5: 5,
                            pygame.K_6: 6,
                            pygame.K_7: 7,
                            pygame.K_8: 8,
                            pygame.K_9: 9,
                        }
                        if (
                            event.key in key_to_num
                            and sudoku.full_board[r][c] == key_to_num[event.key]
                        ):
                            sudoku.board[r][c] = key_to_num[event.key]
                            if find_empty(sudoku.board) is None and not sudoku.cheat:
                                for _ in range(3):
                                    draw_board(sudoku)
                                    pygame.display.flip()
                                    time.sleep(0.5)
                                    screen.fill(WHITE)
                                    victory_text = FONT.render(
                                        "Glückwunsch! Du hast das Sudoku gelöst!",
                                        True,
                                        GREEN,
                                    )
                                    victory_text_rect = victory_text.get_rect(
                                        center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2)
                                    )
                                    screen.blit(victory_text, victory_text_rect)
                                    pygame.display.flip()
                                    time.sleep(0.5)
                                draw_board(sudoku)
                                time.sleep(0.5)
                                screen.fill(WHITE)
                                intermission_text = FONT.render(
                                    "Starte neues Spiel...", True, BLACK
                                )
                                intermission_text_rect = intermission_text.get_rect(
                                    center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2)
                                )
                                screen.blit(intermission_text, intermission_text_rect)
                                pygame.display.flip()
                                time.sleep(2)
                                sudoku.new_game()
                        elif (
                            event.key == pygame.K_BACKSPACE
                            or event.key == pygame.K_DELETE
                        ):
                            sudoku.clear_cell(r, c)
                        elif event.key in key_to_num:
                            sudoku.board[r][c] = "X"
                    else:
                        pass
        draw_board(sudoku)
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def run_sudoku_setup(screen):
    class SudokuSetup(Frame):
        def __init__(self, screen):
            super(SudokuSetup, self).__init__(
                screen,
                screen.height * 3 // 4,
                screen.width * 2 // 3,
                has_border=True,
                hover_focus=True,
                name="setup",
                title="SUDOKU SETUP",
            )

            # Retro-Blau Palette
            self.palette = {
                "background": (0, 0, 4),
                "label": (7, 0, 4),
                "borders": (7, 0, 2),
                "focus_button": (7, 0, 6),
                "button": (7, 0, 3),
                "title": (7, 0, 6),
            }

            self.difficulty = 25
            self.debug_mode = False

            # === Bereich 1: Schwierigkeit ===
            layout_diff = Layout([1])
            self.add_layout(layout_diff)
            layout_diff.add_widget(Label("", align="^"))
            layout_diff.add_widget(Label("SCHWIERIGKEIT", align="^"))
            layout_diff.add_widget(
                Label(
                    "Die Schwierigkeit entscheidet wie viele Felder leer sind.",
                    align="^",
                )
            )

            diff_buttons = Layout([1, 1, 1])
            self.add_layout(diff_buttons)

            def set_diff(level):
                levels = {"Leicht": 5, "Mittel": 25, "Schwer": 35}
                self.difficulty = levels[level]
                self.scene.add_effect(
                    PopUpDialog(screen, f"Schwierigkeit: {level}", ["OK"])
                )

            diff_buttons.add_widget(Button("Leicht", lambda: set_diff("Leicht")), 0)
            diff_buttons.add_widget(Button("Mittel", lambda: set_diff("Mittel")), 1)
            diff_buttons.add_widget(Button("Schwer", lambda: set_diff("Schwer")), 2)
            self.add_layout(Layout([1]))
            self.fix()

            # === Bereich 2: Debug Modus ===
            layout_debug = Layout([1])
            self.add_layout(layout_debug)
            layout_debug.add_widget(Label("", align="^"))
            layout_debug.add_widget(Label("DEBUG MODUS", align="^"))
            layout_debug.add_widget(
                Label(
                    "Erlaubt, dass die Lösungsfunktion das Spiel beendet und somit gewinnt.",
                    align="^",
                )
            )

            debug_layout = Layout([1, 1, 1])
            self.add_layout(debug_layout)
            self.debug_checkbox = CheckBox(
                "Debug aktivieren", on_change=self._toggle_debug
            )
            debug_layout.add_widget(Label("", align="^"), 0)
            debug_layout.add_widget(self.debug_checkbox, 1)
            debug_layout.add_widget(Label("", align="^"), 2)
            self.add_layout(Layout([1]))
            self.fix()

            # === Bereich 3: Abschluss ===
            end_layout = Layout([1, 1])
            self.add_layout(end_layout)
            end_layout.add_widget(Button("Spielen", self._start), 0)
            end_layout.add_widget(Button("Abbrechen", self._exit), 1)

            self.fix()

        def _toggle_debug(self):
            self.debug_mode = self.debug_checkbox.value

        def _start(self):
            global DEBUG, DIFFICULTY
            DEBUG = self.debug_mode
            DIFFICULTY = self.difficulty
            raise StopApplication("Start Game")

        def _exit(self):
            self.scene.add_effect(PopUpDialog(self.screen, "Spiel beendet.", ["OK"]))
            self.screen.refresh()
            time.sleep(0.5)
            sys.exit()

    scenes = [Scene([SudokuSetup(screen)], -1)]
    screen.play(scenes, stop_on_resize=True, start_scene=scenes[0])


if __name__ == "__main__":
    Screen.wrapper(run_sudoku_setup)  # Erst Menü anzeigen

    # Standard Pygame Initialisierung
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Sudoku")
    clock = pygame.time.Clock()

    # Konstanten, die erst nach Initialisierung definiert werden können
    FONT = pygame.font.SysFont(None, 40)
    SMALL_FONT = pygame.font.SysFont(None, 22)

    main()

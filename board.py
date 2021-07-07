from typing import List, Literal
import blessed
from blessed.keyboard import Keystroke
import time  
import tictactoe

from utils import Vec

import logging

logging.basicConfig(filename="logs/debug.log", level=logging.DEBUG)


class Cursor:
    def __init__(self):
        self.cursor = "C"
        self.cell = [0, 0]
        self.cell_loc = [[Vec(0, 0) for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.cell_loc[i][j] = start_pos + cell_size * (i, j) + (i + 1, j + 1)
        self.current_screen_loc = self.cell_loc[self.cell[0]][self.cell[1]]
        self.old_screen_loc = None

    def update(self, direction: Literal["UP", "DOWN", "LEFT", "RIGHT"]):
        new_cell = self.cell[:]
        if direction == "UP":
            new_cell[1] -= 1
        elif direction == "DOWN":
            new_cell[1] += 1
        elif direction == "LEFT":
            new_cell[0] -= 1
        else:
            new_cell[0] += 1

        if (new_cell[0] in (0, 1, 2)) and (new_cell[1] in (0, 1, 2)):
            self.cell = new_cell
            self.old_screen_loc = self.current_screen_loc
            self.current_screen_loc = self.cell_loc[self.cell[0]][self.cell[1]]
            print(
                term.move_xy(*self.old_screen_loc)
                + " "
                + term.move_xy(*self.current_screen_loc)
                + self.cursor,
            )
        else:
            return


# This characters have been used to create the table"
strokes = "│ ─ ┌ ┬ ┐ ├ ┼ ┤ └ ┴ ┘" 
term = blessed.Terminal()

# getting the window size and and board size
window_size = Vec(term.width, term.height)
board_size = Vec(40, 16)
start_pos = (window_size - board_size) / 2
cell_size = (board_size - 4) / 3


def draw_board():
    global board_size, start_pos
    board = term.clear
    top_rule = "┌" + "┬".join("─" * cell_size.x for _ in range(3)) + "┐"
    mid_rule = "├" + "┼".join("─" * cell_size.x for _ in range(3)) + "┤"
    bottom_rule = "└" + "┴".join("─" * cell_size.x for _ in range(3)) + "┘"
    rules = [top_rule, mid_rule, mid_rule, bottom_rule]

    for row in range(board_size.y):
        draw_from = start_pos + (0, row)
        board += term.move_xy(*draw_from)  # type: ignore
        if row % (cell_size.y + 1) == 0:
            board += rules[row // cell_size.y]
            continue
        board += "│" + "│".join(term.move_right(cell_size.x) for _ in range(3)) + "│"  # type: ignore

    print(board)


def update_board(board):
    for i in board:
        #TODO change later after the implement of https://github.com/Anand1310/Bonobos-Tic-Tac-Toe/projects/1#card-64553553
        print(i)


def refresh(val: Keystroke, cursor: Cursor):
    if val.is_sequence:
        name = val.name
        if name[4:] in ("UP", "DOWN", "LEFT", "RIGHT"):
            cursor.update(val.name[4:])  # type: ignore



board = tictactoe.initial_state()
print(f"{term.home}{term.black_on_skyblue}{term.clear}")
cursor = Cursor()
# main event loop
with term.cbreak():
    draw_board()
    cursor.update("UP")
    val = ''
    while val.lower() != 'q' and not tictactoe.terminal(board):
        val = term.inkey(timeout=3)
        refresh(val, cursor)
        #TODO change input method after the implement of https://github.com/Anand1310/Bonobos-Tic-Tac-Toe/projects/1#card-64553566
        if val.isnumeric():
            if int(val) in list(range(1, 10)):

                # Player
                import math
                x = math.ceil(int(val) / 3) - 1
                move = (x, int(val) - 3 * x - 1)
                if move in tictactoe.actions(board):
                    board = tictactoe.move(move)
                    update_board(board)

                    # bot
                    board = tictactoe.move(tictactoe.minimax(board))
                    print("bot is thinking...")
                    time.sleep(5)
                    update_board(board)
    print(term.blink((term.underline_bold_black_on_yellow(f"The winner is ......{tictactoe.winner(board)}"))))
    print(f"bye!{term.normal}")


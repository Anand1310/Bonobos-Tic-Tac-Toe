from typing import List, Literal
import blessed
from blessed.keyboard import Keystroke
import time
import tictactoe
import os
from utils import Vec
from draw_circle import draw_circle, draw_cross

import logging
if "logs" not in os.listdir():
    os.mkdir("logs")
logging.basicConfig(filename="logs/debug.log", level=logging.DEBUG)


class Cursor:
    def __init__(self):
        self.cursor = "->"
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
                + " " * len(self.cursor)
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
board_size = Vec(43, 19)
start_pos = (window_size - board_size) / 2
cell_size = (board_size - 4) / 3

# drawing the frame of the board
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


# drawing XO should happen here
def update_board(board, cursor:Cursor):
    xs = []
    os = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == "X":
                xs.append((i,j))
            elif board[i][j] == "O":
                os.append((i,j))
                
    for x in os:
        x_loc = cursor.cell_loc[x[1]][x[0]]
        center_x, center_y = x_loc + cell_size / 2
        draw_circle(coords=(center_x, center_y), radius=cell_size.y//2, rgb=(0,0,0))
        print(term.on_skyblue)
        
    for x in xs:
        x_loc = cursor.cell_loc[x[1]][x[0]]
        center_x, center_y = x_loc + cell_size / 2
        draw_cross(coords=(center_x, center_y), radius=cell_size.y//2, rgb=(0,0,0))
        print(term.on_skyblue)



def refresh(val: Keystroke, cursor: Cursor):
    if val.is_sequence:
        name = val.name
        if name[4:] in ("UP", "DOWN", "LEFT", "RIGHT"):
            cursor.update(val.name[4:])  # type: ignore
            return
    elif str(val) == " ":
        x, y = cursor.cell
        return (y, x)

    elif val.isnumeric() and (int(val) in list(range(1, 10))):
        import math

        x = math.ceil(int(val) / 3) - 1
        move = (x, int(val) - 3 * x - 1)
        return move
    return


board = tictactoe.initial_state()
print(f"{term.home}{term.black_on_skyblue}{term.clear}")
cursor = Cursor()
# main event loop
with term.cbreak():
    draw_board()
    cursor.update("UP")
    val = ""
    while val.lower() != "q" and not tictactoe.terminal(board):
        val = term.inkey(timeout=3)
        # user input
        move = refresh(val, cursor)
        if move in tictactoe.actions(board):
            board = tictactoe.move(move)
            update_board(board, cursor)  # draw board

            # bot
            board = tictactoe.move(tictactoe.minimax(board))
            print("bot is thinking...")
            time.sleep(5)
            update_board(board, cursor)  # draw board
    print(
        term.blink(
            (
                term.underline_bold_black_on_yellow(
                    f"The winner is ......{tictactoe.winner(board)}"
                )
            )
        )
    )
    print(f"bye!{term.normal}")

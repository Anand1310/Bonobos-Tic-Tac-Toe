from typing import Tuple

import blessed
from blessed.keyboard import Keystroke
import time  
import tictactoe

# I ended up writing this class which has no use except for point.x and point.y
# you can also do arithmatics with these points but same can be done with numpy
class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        return iter((self.x, self.y))

    def __add__(self, other):
        if isinstance(other, Vec):
            return Vec(self.x + other.x, self.y + other.y)
        elif isinstance(other, int):
            return Vec(self.x + other, self.y + other)
        elif (
            isinstance(other, Tuple)
            and isinstance(other[0], int)
            and isinstance(other[1], int)
        ):
            return Vec(self.x + other[0], self.y + other[1])
        else:
            raise ValueError(f"Can not add Position with {type(other)}")

    def __sub__(self, other):
        if isinstance(other, Vec):
            return Vec(self.x - other.x, self.y - other.y)
        elif isinstance(other, int):
            return Vec(self.x - other, self.y - other)
        elif (
            isinstance(other, Tuple)
            and isinstance(other[0], int)
            and isinstance(other[1], int)
        ):
            return Vec(self.x - other[0], self.y - other[1])
        else:
            raise ValueError(f"Can not add Position with {type(other)}")

    def __truediv__(self, other):
        if isinstance(other, Vec):
            return Vec(self.x // other.x, self.y // other.y)
        elif isinstance(other, int):
            return Vec(self.x // other, self.y // other)
        elif (
            isinstance(other, Tuple)
            and isinstance(other[0], int)
            and isinstance(other[1], int)
        ):
            return Vec(self.x // other[0], self.y // other[1])
        else:
            raise ValueError(f"Can not add Position with {type(other)}")

    def __floordiv__(self, other):
        return self.__truediv__(self, other)

    def __mul__(self, other):
        if isinstance(other, Vec):
            return Vec(self.x * other.x, self.y * other.y)
        elif isinstance(other, int):
            return Vec(self.x * other, self.y * other)
        elif (
            isinstance(other, Tuple)
            and isinstance(other[0], int)
            and isinstance(other[1], int)
        ):
            return Vec(self.x * other[0], self.y * other[1])
        else:
            raise ValueError(f"Can not add Position with {type(other)}")

    def __repr__(self) -> str:
        return f"Position({self.x}, {self.y})"


# This characters have been used to create the table"
strokes = "│ ─ ┌ ┬ ┐ ├ ┼ ┤ └ ┴ ┘" 
term = blessed.Terminal()

# getting the window size and and board size
window_size = Vec(term.width, term.height)
board_size = Vec(40, 16)

# actual function that draws the board
def draw_board(shape: Vec):
    start_pos = (window_size - shape) / 2
    board = term.clear
    cell_size = (shape - 4) / 3
    top_rule = "┌" + "┬".join("─" * cell_size.x for _ in range(3)) + "┐"
    mid_rule = "├" + "┼".join("─" * cell_size.x for _ in range(3)) + "┤"
    bottom_rule = "└" + "┴".join("─" * cell_size.x for _ in range(3)) + "┘"
    rules = [top_rule, mid_rule, mid_rule, bottom_rule]

    for row in range(shape.y):
        cur_pos = start_pos + (0, row)
        board += term.move_xy(*cur_pos)  # type: ignore
        if row % (cell_size.y + 1) == 0:
            board += rules[row // cell_size.y]
            continue
        board += "│" +"│".join(term.move_right(cell_size.x) for _ in range(3)) + "│"  # type: ignore

    print(board)

def update_board(board):
    for i in board:
        #TODO change later after the implement of https://github.com/Anand1310/Bonobos-Tic-Tac-Toe/projects/1#card-64553553
        print(i)

# Things to do at each frame
def refresh(val: Keystroke):
    if val.is_sequence:
        # no use
        print("got sequence: {0}.".format((str(val), val.name, val.code)))


print("press 'q' to quit.")
print(f"{term.home}{term.black_on_skyblue}{term.clear}") # clear screen
draw_board(board_size)

board = tictactoe.initial_state()
# main event loop
with term.cbreak():
    val = ''
    while val.lower() != 'q' and not tictactoe.terminal(board):
        val = term.inkey(timeout=3)
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


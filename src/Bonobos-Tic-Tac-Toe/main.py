import blessed
import numpy as np  # im using numpy, as its fast. you could also use normal list
import time
import atexit

pos_X = []  # contains all the positions of X
pos_O = []  # contains all the positions of O


# initialising the frame and terminal. and setting our frame size to termnal size
term = blessed.Terminal()
frame = np.array([[""] * term.width] * term.height)

# the size btw the lines


def draw_frame(term, frame):  # see the documentation of numpy for np.where
    ys, xs = np.where(frame == "█")
    r = term.clear
    for y, x in zip(ys, xs):
        r = r + term.move_xy(int(x), int(y)) + "█"
        frame[int(y), int(x)] = ""
    print(r, end="")
    return frame, term


def draw_table(frame, X=None, O=None, padding=10):
    size = term.width // 2 - 10
    for i in range(len(frame)):
        if (i > padding // 2) and (i < (term.height - padding // 2)):
            frame[i][size] = "█"
            frame[i][term.width - size] = "█"
    padding = int(padding * term.width / term.height)
    size = (term.height // 2 - 10) * 2
    for j in range(len(frame[size])):
        if (j > padding) and (j < term.width - padding):
            frame[size][j] = "█"
            frame[abs(term.height - size)][j] = "█"
    draw_frame(term, frame)


draw_table(frame)

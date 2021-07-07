from typing import Tuple
from blessed import Terminal
from math import sqrt

term = Terminal()

def draw_curve(center_x, center_y, x, y):
        print(f"{term.move_xy(center_x+x, center_y+y)} ")
        print(f"{term.move_xy(center_x+x, center_y-y)} ")
        print(f"{term.move_xy(center_x-x, center_y+y)} ")
        print(f"{term.move_xy(center_x-x, center_y-y)} ")

def draw_circle(center_x: int, center_y: int,
                radius: int, rgb: Tuple=(0,255,0)):
    """
    Draws a circle of a given radius at point center_x, center_y.
    Will be painted green if no RGB tuple is given.
    """
    r2 = radius ** 2
    y = radius
    x = 1

    print(term.on_color_rgb(*rgb))
    print(f"{term.move_xy(center_x, center_y+radius) } ")
    print(f"{term.move_xy(center_x, center_y-radius) } ")
    print(f"{term.move_xy(center_x+radius, center_y) } ")
    print(f"{term.move_xy(center_x-radius, center_y) } ")
    while x < y:
        y = int(sqrt(r2 - x ** 2) + 0.5)
        draw_curve(center_x, center_y, x, y)
        x += 1
    while y > 0:
        x = int(sqrt(r2 - y ** 2) + 0.5)
        draw_curve(center_x, center_y, x, y)
        y -= 1
    
def main(x: int, y: int, radius: int):
    import atexit

    @atexit.register
    def Goodbye():
        print(term.normal+term.home+term.clear, end="")

    print(term.home + term.clear, end='')
    print(f"{term.on_grey} ", end="")
    draw_circle(x, y, radius)

    with term.cbreak():
        val=""
        while val.lower() != "q":
            val = term.inkey(timeout=3)
            continue

if __name__ == "__main__":
    main(15, 15, 12)

from typing import Tuple
from blessed import Terminal
from math import sqrt

term = Terminal()

def draw_curve(center_x, center_y, x, y, fill):
    print(f"{term.move_xy(center_x+x, center_y+y)}{fill}")
    print(f"{term.move_xy(center_x+x, center_y-y)}{fill}")
    print(f"{term.move_xy(center_x-x, center_y+y)}{fill}")
    print(f"{term.move_xy(center_x-x, center_y-y)}{fill}")

def draw_circle(coords: Tuple, radius: int,
                rgb: Tuple=(0,255,0), fill: str="  "):
    """
    Draws a circle of a given radius at point center_x, center_y.
    Will be painted green if no RGB tuple is given.
    """
    r2 = radius ** 2
    cx, cy = coords
    y = radius
    x = 1

    print(term.on_color_rgb(*rgb))
    print(f"{term.move_xy(cx, cy+radius)}{fill}")
    print(f"{term.move_xy(cx, cy-radius)}{fill}")
    print(f"{term.move_xy(cx+radius*2, cy)}{fill}")
    print(f"{term.move_xy(cx-radius*2, cy)}{fill}")

    while x < y:
        y = int(sqrt(r2 - x ** 2) + 0.5)
        draw_curve(cx, cy, x*2, y, fill)
        x += 1
    while y > 0:
        x = int(sqrt(r2 - y ** 2) + 0.5)
        draw_curve(cx, cy, x*2, y, fill)
        y -= 1

def main():
    import atexit

    @atexit.register
    def Goodbye():
        print(term.normal+term.home+term.clear, end="")

    coords = 30,8
    radius = 8

    print(term.home + term.clear, end='')
    print(f"{term.on_grey} ", end="")

    # draw_circle(coords, radius)
    for i in range(1, radius, 2):
        draw_circle(coords, i)

    with term.cbreak():
        val=""
        while val.lower() != "q":
            val = term.inkey(timeout=3)
            continue

if __name__ == "__main__":
    main()

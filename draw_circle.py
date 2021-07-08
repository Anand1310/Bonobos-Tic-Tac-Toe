from typing import Tuple
from blessed import Terminal
from math import sqrt

term = Terminal()

def draw_curve(center_x, center_y, x, y, fill):
    print(f"{term.move_xy(center_x+x, center_y+y)}{fill}")
    print(f"{term.move_xy(center_x+x, center_y-y)}{fill}")
    print(f"{term.move_xy(center_x-x, center_y+y)}{fill}")
    print(f"{term.move_xy(center_x-x, center_y-y)}{fill}")

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
    print(f"{term.move_xy(center_x-1, center_y+radius) }   ")
    print(f"{term.move_xy(center_x-1, center_y-radius) }   ")
    print(f"{term.move_xy(center_x+radius*2, center_y) }  ")
    print(f"{term.move_xy(center_x-radius*2-1, center_y) }  ")

    while x < y:
        y = int(sqrt(r2 - x ** 2) + 0.5)
        draw_curve(center_x, center_y, x*2, y)
        draw_curve(center_x, center_y, x*2+1, y)
        x += 1
    while y > 0:
        x = int(sqrt(r2 - y ** 2) + 0.5)
        draw_curve(center_x, center_y, x*2, y)
        draw_curve(center_x, center_y, x*2+1, y)

        y -= 1

def main():
    import atexit

    @atexit.register
    def Goodbye():
        print(term.normal+term.home+term.clear, end="")

    x = 30
    y = 15
    radius = 14

    print(term.home + term.clear, end='')
    print(f"{term.on_grey} ", end="")

    for i in range(1, radius, 2):
        draw_circle(x, y, i)

    with term.cbreak():
        val=""
        while val.lower() != "q":
            val = term.inkey(timeout=3)
            continue

if __name__ == "__main__":
    main()

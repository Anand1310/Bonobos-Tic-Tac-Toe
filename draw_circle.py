from typing import Tuple
from blessed import Terminal
from math import sqrt

END_LOGIC = ((0,0,1,-1), (1,-1,0,0))
CURVE_LOGIC = ((1,1,-1,-1), (1,-1,1,-1))

term = Terminal()

def draw_curve(cx, cy, x, y, fill, logic=CURVE_LOGIC):
    pixels = []
    for i in range(4):
        coords = (cx+x*logic[0][i], cy+y*logic[1][i])
        pixels.append(f"{term.move_xy(*coords)}{fill}")
    return pixels

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
    circle = []

    circle.append(term.on_color_rgb(*rgb)) #colour
    circle.extend(draw_curve(cx, cy, radius*2, radius, fill, logic=END_LOGIC))
    while x < y:
        y = int(sqrt(r2 - x ** 2) + 0.5)
        circle.extend(draw_curve(cx, cy, x*2, y, fill))
        x += 1
    while y > 0:
        x = int(sqrt(r2 - y ** 2) + 0.5)
        circle.extend(draw_curve(cx, cy, x*2, y, fill))
        y -= 1
    print("".join(circle))

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

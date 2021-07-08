from typing import Tuple
from blessed import Terminal
from math import sqrt

END_LOGIC = ((0,0,1,-1), (1,-1,0,0))
CURVE_LOGIC = ((1,1,-1,-1), (1,-1,1,-1))

term = Terminal()

def draw_curve(cx, cy, x, y, fill, logic=CURVE_LOGIC) -> list:
    """
    Draws a rotationally symmetrical curve based on curve logic.
    """
    pixels = []
    for i in range(4):
        coords = (cx + x*logic[0][i], cy + y*logic[1][i])
        pixels.append(f"{term.move_xy(*coords)}{fill}")
    return pixels

def draw_circle(coords: Tuple, radius: int,
                rgb: Tuple=(0,255,0), fill: str="██") -> None:
    """
    Draws a circle of a given radius at point center_x, center_y.
    Will be painted green if no RGB tuple is given.
    """
    r2 = radius ** 2
    cx, cy = coords
    y = radius
    x = 1
    circle = []

    circle.append(term.color_rgb(*rgb)) #colour
    circle.extend(draw_curve(*coords, radius*2, radius, fill, logic=END_LOGIC))
    while x < y:
        y = int(sqrt(r2 - x**2) + 0.5)
        circle.extend(draw_curve(*coords, x*2, y, fill))
        x += 1
    while y > 0:
        x = int(sqrt(r2 - y**2) + 0.5)
        circle.extend(draw_curve(*coords, x*2, y, fill))
        y -= 1
    print("".join(circle))

def draw_cross(coords: Tuple, radius: int,
                rgb: Tuple=(0,255,0), fill: str="██") -> None:
    """
    Draws a cross of a given radius at coords.
    Will be painted green if no RGB tuple is given.
    """
    cross = []
    cross.append(term.color_rgb(*rgb))
    cross.append(f"{term.move_xy(*coords)}{fill}")
    for i in range(1, radius):
        cross.extend(draw_curve(*coords, i*2, i, fill))
    print("".join(cross))

def main():
    import atexit

    @atexit.register
    def Goodbye():
        print(term.normal+term.home+term.clear, end="")

    coords = 20,10
    radius = 8

    print(term.home + term.clear, end='')
    print(f"{term.on_grey} ", end="")
    rgb = [(255,0,0),(0,255,0)]
    draw_circle(coords, radius)

    for i in range(1, radius+1, 2):
        draw_circle((60, 10), i)

    for i in range(0, radius+1, 1):
        draw_circle((100, 10), i, rgb[i%2])
    draw_cross((20, 28), radius)
    with term.cbreak():
        val=""
        while val.lower() != "q":
            val = term.inkey(timeout=3)
            continue

if __name__ == "__main__":
    main()
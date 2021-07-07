from typing import Tuple


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
    

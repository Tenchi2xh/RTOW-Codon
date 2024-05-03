from math import sqrt
from typing import List, Tuple

from .ppm import save
from .interval import Interval
from .vec3 import Color


intensity = Interval(0.000, 0.999)

def linear_to_gamma_8bit(linear: float) -> UInt[8]:
    linear = sqrt(linear) if linear > 0 else 0
    return UInt[8](256 * intensity.clamp(linear))


class Buffer:
    w: int
    h: int
    buffer: List[List[Color]]

    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h
        self.buffer = [[Color() for x in range(w)] for y in range(h)]

    def save_ppm(self, name: str):
        save(self.raw_buffer(), name)

    def __getitem__(self, i: int) -> List[Color]:
        return self.buffer[i]

    def __setitem__(self, y: int, row: List[Color]):
        assert len(row) == self.w, "Invalid row length"
        self.buffer[y] = row

    def __setitem__(self, xy: Tuple[int, int], c: Color):
        self.buffer[xy[1]][xy[0]] = c

    def raw_buffer(self):
        return [
            [
                (
                    linear_to_gamma_8bit(c.x),
                    linear_to_gamma_8bit(c.y),
                    linear_to_gamma_8bit(c.z),
                )
                for c in row
            ]
            for row in self.buffer
        ]


if __name__ == "__main__":
    b = Buffer(256, 256)
    for y in range(b.h):
        for x in range(b.w):
            b[x, y] = Color(x / (b.w - 1), y / (b.h - 1), 0)
    b.save_ppm("test2")

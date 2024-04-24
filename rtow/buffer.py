from typing import List, Tuple

import ppm
from .vec3 import Color


class Buffer:
    w: int
    h: int
    buffer: List[List[Color]]

    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h
        self.buffer = [[Color() for x in range(w)] for y in range(h)]

    def save_ppm(self, name: str):
        ppm.save(self.raw_buffer(), name)

    def __getitem__(self, i: int) -> List[Color]:
        return self.buffer[i]

    def __setitem__(self, xy: Tuple[int, int], c: Color):
        self.buffer[xy[1]][xy[0]] = c

    def __setitem__(self, y: int, row: List[Color]):
        assert len(row) == self.w, "Invalid row length"
        self.buffer[y] = row

    def raw_buffer(self):
        return [
            [(int(255 * c.x), int(255 * c.y), int(255 * c.z)) for c in row]
            for row in self.buffer
        ]


if __name__ == "__main__":
    b = Buffer(256, 256)
    for y in range(b.h):
        for x in range(b.w):
            b[x, y] = Color(x / (b.w - 1), y / (b.h - 1), 0)
    b.save_ppm("test2")

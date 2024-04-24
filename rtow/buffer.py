from typing import List, Tuple

import ppm
from .vec3 import Color


class Buffer:
    w: int
    h: int
    format: str
    name: str
    buffer: List[List[Color]]

    def __init__(self, w: int, h: int, name: str, format: str):
        self.w = w
        self.h = h
        self.name = name
        self.format = format
        self.buffer = [[Color() for x in range(w)] for y in range(h)]

    def __enter__(self):
        return self

    def __exit__(self):
        if self.format == "ppm":
            ppm.save(self.raw_buffer(), self.name)

    def __getitem__(self, i: int) -> List[Color]:
        return self.buffer[i]

    def __setitem__(self, xy: Tuple[int, int], c: Color):
        self.buffer[xy[1]][xy[0]] = c

    def __setitem__(self, y: int, row: List[Color]):
        self.buffer[y] = row

    def raw_buffer(self):
        return [
            [(int(255 * c.x), int(255 * c.y), int(255 * c.z)) for c in row]
            for row in self.buffer
        ]


if __name__ == "__main__":
    with Buffer(256, 256, "test2", "ppm") as b:
        for y in range(b.h):
            for x in range(b.w):
                b[x, y] = Color(x / (b.w - 1), y / (b.h - 1), 0)

from typing import List, Tuple


class CoordChunk:
    x0: int
    x1: int
    y0: int
    y1: int

    def __init__(self, x0, x1, y0, y1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

    @property
    def width(self):
        return self.x1 - self.x0

    @property
    def height(self):
        return self.y1 - self.y0


def create_coordinate_chunks(width: int, height: int, chunk_size: int) -> List[CoordChunk]:
    chunks: List[CoordChunk] = []

    for y in range(0, height, chunk_size):
        for x in range(0, width, chunk_size):
            chunks.append(
                CoordChunk(
                    x0=x,
                    x1=min(x + chunk_size, width),
                    y0=y,
                    y1=min(y + chunk_size, height),
                )
            )

    return chunks
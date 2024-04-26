import os
from typing import List, Tuple


def save(buffer: List[List[Tuple[UInt[8], UInt[8], UInt[8]]]], name: str):
    assert len(buffer) > 0
    width = len(buffer[0])
    height = len(buffer)

    os.system("mkdir -p renders")
    with open(f"renders/{name}.ppm", "w") as f:
        f.write("P3\n")
        f.write(f"{width} {height} 255\n")
        for row in buffer:
            for pixel in row:
                f.write(" ".join(str(c) for c in pixel) + "\n")


if __name__ == "__main__":
    w = 256
    buffer = [
        [(UInt[8](255 * x / (w - 1)), UInt[8](255 * y / (w - 1)), UInt[8](0)) for x in range(w)]
        for y in range(w)
    ]

    save(buffer, "test")

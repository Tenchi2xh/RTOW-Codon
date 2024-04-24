from typing import List, Tuple


def save(buffer: List[List[Tuple[int, int, int]]], name: str):
    assert len(buffer) > 0
    width = len(buffer[0])
    height = len(buffer)

    with open(f"{name}.ppm", "w") as f:
        f.write("P3\n")
        f.write(f"{width} {height} 255\n")
        for row in buffer:
            for pixel in row:
                f.write(" ".join(str(c) for c in pixel) + "\n")


if __name__ == "__main__":
    w = 256
    buffer = [
        [(int(255 * x / (w - 1)), int(255 * y / (w - 1)), 0) for x in range(w)]
        for y in range(w)
    ]

    save(buffer, "test")

from typing import List, Tuple

from .vec3 import Color


@python # type: ignore
def load_image(image_filename: str) -> List[List[Tuple[int, int, int]]]:
    from PIL import Image

    image = Image.open(image_filename).convert("RGB")
    width, height = image.size
    data = list(image.getdata())

    pixels = [data[i * width:(i + 1) * width] for i in range(height)]
    return pixels


def clamp(x: int, low: int, high: int):
    # Return the value clamped to the range [low, high)
    if x < low: return low
    if x < high: return x
    return high - 1


def linearize(x: int) -> float:
    return (x / 255.0)**2.2


class Image:
    width: int
    height: int
    colors: List[List[Color]]

    def __init__(self, image_filename):
        pixels = load_image(image_filename)
        self.height = len(pixels)
        self.width = len(pixels[0])

        # TODO: Might need to do gamma correction

        self.colors = [
            [Color(linearize(pixel[0]), linearize(pixel[1]), linearize(pixel[2])) for pixel in row]
            for row in pixels
        ]

    def __getitem__(self, xy: Tuple[int, int]) -> Color:
        x, y = xy
        x = clamp(x, 0, self.width)
        y = clamp(y, 0, self.height)

        return self.colors[y][x]


if __name__ == "__main__":
    image = Image("images/earthmap.jpg")
    print(image.width, image.height)
    print(image[0, 0])

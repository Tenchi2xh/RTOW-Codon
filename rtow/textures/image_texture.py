from .texture import Texture
from .. import Point3, Color, Image, Interval


class ImageTexture(Texture):
    image: Image

    def __init__(self, image_filename: str):
        self.image = Image(image_filename)

    def value(self, u: float, v: float, p: Point3) -> Color:
        # If we have no texture data, then return solid cyan as a debugging aid
        if self.image.height <= 0:
            return Color(0, 1, 1)

        # Clamp input texture coordinates to [0,1] x [1,0]
        u = Interval(0, 1).clamp(u)
        v = 1.0 - Interval(0,1).clamp(v)  # Flip V to image coordinates

        i = int(u * self.image.width)
        j = int(v * self.image.height)

        return self.image[i, j]

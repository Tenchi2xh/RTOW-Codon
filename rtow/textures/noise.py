from .texture import Texture
from .. import Point3, Color, Perlin


class NoiseTexture(Texture):
    noise: Perlin
    scale: float

    def __init__(self, scale = 1.0):
        self.noise = Perlin()
        self.scale = scale

    def value(self, u: float, v: float, p: Point3) -> Color:
        return Color(1, 1, 1) * self.noise.noise(self.scale * p)

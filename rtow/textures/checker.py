from math import floor

from .texture import Texture
from .solid_color import SolidColor
from .. import Color, Point3

class Checker(Texture):
    inv_scale: float
    even: Texture
    odd: Texture

    def __init__(self, scale: float, even: Texture, odd: Texture):
        self.inv_scale = 1.0 / scale
        self.even = even
        self.odd = odd

    @staticmethod
    def from_colors(scale: float, even: Color, odd: Color):
        return Checker(scale, SolidColor(even), SolidColor(odd))

    def value(self, u: float, v: float, p: Point3) -> Color:
        x = floor(self.inv_scale * p.x)
        y = floor(self.inv_scale * p.y)
        z = floor(self.inv_scale * p.z)

        is_even = (x + y + z) % 2 == 0

        return (self.even if is_even else self.odd).value(u, v, p)

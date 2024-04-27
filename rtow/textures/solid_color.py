from .texture import Texture
from .. import Point3, Color


class SolidColor(Texture):
    albedo: Color

    def __init__(self, albedo: Color):
        self.albedo = albedo

    @staticmethod
    def from_rgb(red: float, green: float, blue: float):
        return SolidColor(Color(red, green, blue))

    def value(self, u: float, v: float, p: Point3) -> Color:
        return self.albedo

from .vec3 import Vec3


class Color(Vec3):
    r: float
    g: float
    b: float

    def __init__(self, r: float = 0, g: float = 0, b: float = 0):
        super().__init__(r, g, b)
        self.r = r
        self.g = g
        self.b = b

    @staticmethod
    def gray(intensity: float):
        return Color(intensity, intensity, intensity)


black = Color(0, 0, 0)
white = Color(1, 1, 1)

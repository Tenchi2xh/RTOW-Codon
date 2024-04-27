from .. import Point3, Color


class Texture:
    def value(self, u: float, v: float, p: Point3) -> Color:
        assert False, "Calling abstract"

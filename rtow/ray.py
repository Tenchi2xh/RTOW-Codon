from .vec3 import Point3, Vec3

class Ray:
    origin: Point3
    direction: Vec3
    time: float

    def __init__(self, orig: Point3, dir: Vec3):
        self.origin = orig
        self.direction = dir
        self.time = 0

    def __init__(self, orig: Point3, dir: Vec3, time: float):
        self.origin = orig
        self.direction = dir
        self.time = time

    def at(self, t: float):
        return self.origin + t * self.direction

    def __repr__(self):
        return f"Ray(orig={self.origin}, dir={self.direction})"


if __name__ == "__main__":
    print(Ray())
    print(Ray(Point3(), Vec3(0, 1, 0)).at(2))

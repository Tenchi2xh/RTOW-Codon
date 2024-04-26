from .vec3 import Point3, Vec3

class Ray:
    orig: Point3
    dir: Vec3

    def __init__(self, orig: Point3, dir: Vec3):
        self.orig = orig
        self.dir = dir

    def at(self, t: float):
        return self.orig + t * self.dir

    def __repr__(self):
        return f"Ray(orig={self.orig}, dir={self.dir})"


if __name__ == "__main__":
    print(Ray())
    print(Ray(Point3(), Vec3(0, 1, 0)).at(2))

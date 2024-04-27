from math import sqrt
from random import random, uniform

s: float = 1e-8


class Vec3:
    x: float
    y: float
    z: float

    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x, self.y, self.z = x, y, z

    def axis(self, n: int):
        if n == 1: return self.y
        if n == 2: return self.z
        return self.x

    def __repr__(self):
        return f"<{self.x}, {self.y}, {self.z}>"

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __add__(self, other: Vec3):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __radd__(self, other: Vec3):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vec3):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Vec3):
        return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __mul__(self, scalar: float):
        return Vec3(scalar * self.x, scalar * self.y, scalar * self.z)

    # <python-only>
    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        return Vec3(other * self.x, other * self.y, other * self.z)
    # </python-only>

    def __rmul__(self, scalar: float):
        return Vec3(scalar * self.x, scalar * self.y, scalar * self.z)

    def __truediv__(self, scalar: float):
        return self * (1 / scalar)

    def length(self) -> float:
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z

    def near_zero(self) -> bool:
        return abs(self.x) < s and abs(self.y) < s and abs(self.z) < s

    def dot(self, other: Vec3):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vec3):
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def unit(self):
        return self / self.length()
    
    def reflect(self, normal: Vec3):
        return self - 2 * self.dot(normal) * normal

    def refract(self, normal: Vec3, index_ratio: float):
        cos_theta = min(-self.dot(normal), 1.0)
        r_out_perp = index_ratio * (self + cos_theta * normal)
        r_out_parallel = -sqrt(abs(1.0 - r_out_perp.length_squared())) * normal
        return r_out_perp + r_out_parallel

    @staticmethod
    def random():
        return Vec3(random(), random(), random())

    @staticmethod
    def random(min: float = 0, max: float = 1):
        return Vec3(uniform(min, max), uniform(min, max), uniform(min, max))

    @staticmethod
    def random_in_unit_sphere():
        while True:
            p = Vec3.random(-1.0, 1.0)
            if p.length_squared() < 1:
                return p

    @staticmethod
    def random_in_unit_disk():
        while True:
            p = Vec3(uniform(-1.0, 1.0), uniform(-1.0, 1.0), 0)
            if p.length_squared() < 1:
                return p

    @staticmethod
    def random_unit():
        return Vec3.random_in_unit_sphere().unit()

    @staticmethod
    def random_on_hemisphere(normal: Vec3):
        on_unit_sphere = Vec3.random_unit()
        if on_unit_sphere.dot(normal) > 0.0:  # In the same hemisphere as the normal
            return on_unit_sphere
        return -on_unit_sphere


Point3 = Vec3
Color = Vec3


if __name__ == "__main__":
    vec = Vec3(1, 2, 3)

    print("---")
    print("Vec(1, 2, 3)")
    print(vec)

    print("---")
    print("-Vec(1, 2, 3)")
    print(-vec)

    print("---")
    print("Vec(1, 2, 3).length()")
    print(vec.length())

    print("---")
    print("Vec(1, 2, 3) + Vec3(1, 1, 1)")
    print(vec + Vec3(1, 1, 1))

    print("---")
    print("Vec(1, 2, 3) - Vec3(1, 1, 1)")
    print(vec - Vec3(1, 1, 1))

    print("---")
    print("Vec(1, 2, 3) * Vec3(2, 2, 2)")
    print(vec * Vec3(2, 2, 2))

    print("---")
    print("Vec(1, 2, 3) * 2")
    print(vec * 2)

    print("---")
    print("2 * Vec(1, 2, 3)")
    print(2 * vec)

    print("---")
    print("Vec(1, 2, 3) / 2")
    print(vec / 2)

    print("---")
    print("Vec(1, 2, 3).dot(Vec3(2, 2, 2))")
    print(vec.dot(Vec3(2, 2, 2)))

    print("---")
    print("Vec(1, 2, 3).cross(Vec(2, 2, 2))")
    print(vec.cross(Vec3(2, 2, 2)))

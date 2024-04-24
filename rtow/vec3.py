from math import sqrt

class Vec3:
    x: float
    y: float
    z: float

    def __init__(self):
        self.x, self.y, self.z = 0, 0, 0

    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = x, y, z

    def __repr__(self):
        return f"<{self.x}, {self.y}, {self.z}>"

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __add__(self, other: Vec3):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vec3):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Vec3):
        return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __mul__(self, scalar: float):
        return Vec3(scalar * self.x, scalar * self.y, scalar * self.z)

    def __truediv__(self, scalar: float):
        return self * (1 / scalar)

    def length(self) -> float:
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z

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


@extend # type: ignore
class int:
    def __mul__(self, vec3: Vec3):
        return vec3 * self

@extend # type: ignore
class float:
    def __mul__(self, vec3: Vec3):
        return vec3 * self


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
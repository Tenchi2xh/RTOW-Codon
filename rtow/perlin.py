from random import random, shuffle
from typing import List

from .vec3 import Point3


point_count: int = 256


def generate_perm():
    p = [i for i in range(point_count)]
    shuffle(p)
    return p


def trilinear(kernel: List[List[List[float]]], dx: float, dy: float, dz: float) -> float:
    accu = 0.0
    for i in range(2):
        for j in range(2):
            for k in range(2):
                accu += (
                    (i * dx + (1 - i) * (1 - dx)) *
                    (j * dy + (1 - j) * (1 - dy)) *
                    (k * dz + (1 - k) * (1 - dz)) *
                    kernel[i][j][k]
                )
    return accu


class Perlin:
    randfloat: List[float]
    perm_x: List[int]
    perm_y: List[int]
    perm_z: List[int]

    def __init__(self):
        self.randfloat = [random() for _ in range(point_count)]
        self.perm_x = generate_perm()
        self.perm_y = generate_perm()
        self.perm_z = generate_perm()

    def noise(self, p: Point3) -> float:
        xx, dx = divmod(p.x, 1)
        yy, dy = divmod(p.y, 1)
        zz, dz = divmod(p.z, 1)

        dx = dx * dx * (3 - 2 * dx)
        dy = dy * dy * (3 - 2 * dy)
        dz = dz * dz * (3 - 2 * dz)

        kernel = [
            [
                [
                    self.randfloat[
                        self.perm_x[int(xx + i) & 255] ^
                        self.perm_y[int(yy + j) & 255] ^
                        self.perm_z[int(zz + k) & 255]
                    ]
                    for k in range(2)
                ]
                for j in range(2)
            ]
            for i in range(2)
        ]

        return trilinear(kernel, dx, dy, dz)

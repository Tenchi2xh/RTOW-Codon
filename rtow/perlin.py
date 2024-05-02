from random import random, shuffle
from typing import List

from .vec3 import Point3, Vec3


point_count: int = 256


def generate_perm():
    p = [i for i in range(point_count)]
    shuffle(p)
    return p


def trilinear(kernel: List[List[List[Vec3]]], dx: float, dy: float, dz: float) -> float:
    # Hermite cubic smoothing
    dx_h = dx * dx * (3 - 2 * dx)
    dy_h = dy * dy * (3 - 2 * dy)
    dz_h = dz * dz * (3 - 2 * dz)

    accu = 0.0
    for i in range(2):
        for j in range(2):
            for k in range(2):
                weight_v = Vec3(dx - i, dy - j, dz - k)
                accu += (
                    (i * dx_h + (1 - i) * (1 - dx_h)) *
                    (j * dy_h + (1 - j) * (1 - dy_h)) *
                    (k * dz_h + (1 - k) * (1 - dz_h)) *
                    kernel[i][j][k].dot(weight_v)
                )
    return accu


class Perlin:
    randvec: List[Vec3]
    perm_x: List[int]
    perm_y: List[int]
    perm_z: List[int]

    def __init__(self):
        self.randvec = [Vec3.random(-1, 1) for _ in range(point_count)]
        self.perm_x = generate_perm()
        self.perm_y = generate_perm()
        self.perm_z = generate_perm()

    def noise(self, p: Point3) -> float:
        xx, dx = divmod(p.x, 1)
        yy, dy = divmod(p.y, 1)
        zz, dz = divmod(p.z, 1)

        kernel = [
            [
                [
                    self.randvec[
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

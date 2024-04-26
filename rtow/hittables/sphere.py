from math import sqrt
from typing import Optional

from .. import Point3, Ray, Interval, Hittable, Hit, Material, HitMat, Vec3


class Sphere(Hittable):
    center0: Point3
    radius: float
    mat: Material
    is_moving: bool
    direction: Vec3

    # Stationary sphere
    def __init__(self, center: Point3, radius: float, mat: Material):
        self.center0 = center
        self.radius = max(0, radius)
        self.mat = mat
        self.is_moving = False

    # Moving sphere
    def __init__(self, center0: Point3, center1: Point3, radius: float, mat: Material):
        self.center0 = center0
        self.radius = max(0, radius)
        self.mat = mat
        self.is_moving = True
        self.direction = center1 - center0

    def center(self, time: float):
        return self.center0 + time * self.direction

    def hit(self, r: Ray, interval: Interval) -> Optional[HitMat]:
        center = self.center(r.time) if self.is_moving else self.center0
        oc = center - r.origin
        a = r.direction.length_squared()
        h = r.direction.dot(oc)
        c = oc.length_squared() - self.radius * self.radius

        discriminant = h * h - a * c
        if discriminant < 0:
            return None

        sqrtd = sqrt(discriminant)

        # Find the nearest root that lies in the acceptable range
        root = (h - sqrtd) / a
        if not interval.surrounds(root):
            root = (h + sqrtd) / a
            if not interval.surrounds(root):
                return None

        p = r.at(root)
        return HitMat(
            hit=Hit(
                p=p,
                t=root,
                outward_normal=(p - center) / self.radius,
                r=r,
            ),
            mat=self.mat
        )

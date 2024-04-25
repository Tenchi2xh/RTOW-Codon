from math import sqrt
from typing import Optional, Tuple

from .. import Point3, Ray, Interval, Hittable, Hit, Material, HitMat


class Sphere(Hittable):
    center: Point3
    radius: float
    mat: Material

    def __init__(self, center: Point3, radius: float, mat: Material):
        self.center = center
        self.radius = max(0, radius)
        self.mat = mat

    def hit(self, r: Ray, interval: Interval) -> Optional[HitMat]:
        oc = self.center - r.orig
        a = r.dir.length_squared()
        h = r.dir.dot(oc)
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
                outward_normal=(p - self.center) / self.radius,
                r=r,
            ),
            mat=self.mat
        )

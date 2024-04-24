from math import sqrt
from typing import Optional

from .. import Hittable, Hit, Point3, Ray, Interval


class Sphere(Hittable):
    center: Point3
    radius: float

    def __init__(self, center: Point3, radius: float):
        self.center = center
        self.radius = max(0, radius)

    def hit(self, r: Ray, interval: Interval) -> Optional[Hit]:
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
        return Hit(
            p=p,
            t=root,
            outward_normal=(p - self.center) / self.radius,
            r=r,
        )

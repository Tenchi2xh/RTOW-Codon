from typing import Optional

from .ray import Ray
from .vec3 import Point3
from .interval import Interval


class AABB:
    x: Interval
    y: Interval
    z: Interval

    def __init__(self, x: Interval = Interval(), y: Interval = Interval(), z: Interval = Interval()):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def from_points(a: Point3, b: Point3):
        # Treat the two points a and b as extrema for the bounding box, so we don't require a
        # particular minimum/maximum coordinate order
        return AABB(
            x=Interval(a.x, b.x) if a.x <= b.x else Interval(b.x, a.x),
            y=Interval(a.y, b.y) if a.y <= b.y else Interval(b.y, a.y),
            z=Interval(a.z, b.z) if a.z <= b.z else Interval(b.z, a.z),
        )

    @staticmethod
    def from_aabbs(box0: AABB, box1: AABB):
        return AABB(
            x=Interval.from_intervals(box0.x, box1.x),
            y=Interval.from_intervals(box0.y, box1.y),
            z=Interval.from_intervals(box0.z, box1.z),
        )

    def axis_interval(self, n: int):
        if n == 1: return self.y
        if n == 2: return self.z
        return self.x

    def hit(self, r: Ray, ray_t: Interval) -> bool:
        t_min, t_max = ray_t.min, ray_t.max

        for axis in range(3):
            ax = self.axis_interval(axis)
            adinv = 1.0 / r.direction.axis(axis)

            t0 = (ax.min - r.origin.axis(axis)) * adinv
            t1 = (ax.max - r.origin.axis(axis)) * adinv

            if t0 < t1:
                if t0 > t_min: t_min = t0
                if t1 < t_max: t_max = t1
            else:
                if t1 > t_min: t_min = t1
                if t0 < t_max: t_max = t0

            if t_max <= t_min:
                return False

        return True

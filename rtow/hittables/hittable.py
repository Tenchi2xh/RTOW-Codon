from typing import Optional

from .. import Interval, Point3, Vec3, Ray


class Hit:
    p: Point3
    normal: Vec3
    t: float
    front_face: bool

    def __init__(self, p: Point3, outward_normal: Vec3, t: float, r: Ray):
        self.p = p
        self.t = t
        self.front_face = r.dir.dot(outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal


class Hittable:
    def hit(self, r: Ray, interval: Interval) -> Optional[Hit]:
        assert False, "Calling abstract"

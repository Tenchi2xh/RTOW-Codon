from math import sqrt
from typing import Optional

from .. import Point3, Ray, Interval, Hittable, Hit, Material, HitMat, Vec3, AABB


class Sphere(Hittable):
    center0: Point3
    radius: float
    mat: Material
    is_moving: bool
    direction: Vec3
    bbox: AABB

    def __repr__(self):
        return f"<Sphere center={self.center0}>"

    def __init__(self, radius: float, mat: Material, center0: Point3, center1: Optional[Point3] = None):
        self.center0 = center0
        self.radius = max(0, radius)
        self.mat = mat

        rvec = Vec3(radius, radius, radius)

        if center1 is None:
            self.is_moving = False

            rvec = Vec3(radius, radius, radius)
            self.bbox = AABB.from_points(center0 - rvec, center0 + rvec)

        else:
            self.is_moving = True
            self.direction = center1 - center0

            box1 = AABB.from_points(center0 - rvec, center0 + rvec)
            box2 = AABB.from_points(center1 - rvec, center1 + rvec)
            self.bbox = AABB.from_aabbs(box1, box2)


    def center(self, time: float):
        return self.center0 + time * self.direction

    def bounding_box(self) -> AABB:
        return self.bbox

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

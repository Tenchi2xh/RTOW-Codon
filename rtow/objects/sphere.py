from math import acos, atan2, pi, sqrt
from typing import Optional, Tuple

from .. import Point3, Ray, Interval, Vec3, AABB
from .hit import Hit
from .hittable import HitRecord, Hittable
from ..materials import Material


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

    def hit(self, r: Ray, interval: Interval) -> Optional[HitRecord]:
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
        outward_normal = (p - center) / self.radius
        u, v = Sphere.get_uv(outward_normal)

        return HitRecord(
            hit=Hit(
                p=p,
                t=root,
                u=u,
                v=v,
                outward_normal=outward_normal,
                r=r,
            ),
            mat=self.mat
        )

    @staticmethod
    def get_uv(p: Point3) -> Tuple[float, float]:
        # p: a given point on the sphere of radius one, centered at the origin
        # u: returned value [0,1] of angle around the Y axis from X=-1
        # v: returned value [0,1] of angle from Y=-1 to Y=+1
        #     <1 0 0> yields <0.50 0.50>       <-1  0  0> yields <0.00 0.50>
        #     <0 1 0> yields <0.50 1.00>       < 0 -1  0> yields <0.50 0.00>
        #     <0 0 1> yields <0.25 0.50>       < 0  0 -1> yields <0.75 0.50>

        theta = acos(-p.y)
        phi = atan2(-p.z, p.x) + pi

        u = phi / (2 * pi)
        v = theta / pi

        return u, v

from typing import Optional, Tuple

from .ray import Ray
from .vec3 import Color, Point3, Vec3
from .interval import Interval


class Hit:
    p: Point3
    normal: Vec3
    t: float
    front_face: bool

    def __init__(self, p: Point3, outward_normal: Vec3, t: float, r: Ray):
        self.p = p
        self.t = t
        self.front_face = r.direction.dot(outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal


class Scatter:
    attenuation: Color
    scattered: Ray

    def __init__(self, attenuation: Color, scattered: Ray):
        self.attenuation = attenuation
        self.scattered = scattered


class Material:
    def scatter(self, r_in: Ray, hit: Hit) -> Optional[Scatter]:
        assert False, "Calling abstract"


# Codon doesn't support mutually recursive classes
class HitMat:
    hit: Hit
    mat: Material

    def __init__(self, hit: Hit, mat: Material):
        self.hit = hit
        self.mat = mat


class Hittable:
    def hit(self, r: Ray, interval: Interval) -> Optional[HitMat]:
        assert False, "Calling abstract"

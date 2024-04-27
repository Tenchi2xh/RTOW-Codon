from typing import Optional

from .. import Ray, Interval, AABB
from .hit import Hit
from ..materials import Material


# The book puts the material prop inside the hit_record (Hit) class, but Codon doesn't support
# mutually recursive classes or forward declarations (https://github.com/exaloop/codon/issues/482)
# (In our case Hit needs to refer to Material, and Material needs to refer to Hit)
class HitRecord:
    hit: Hit
    mat: Material

    def __init__(self, hit: Hit, mat: Material):
        self.hit = hit
        self.mat = mat


class Hittable:
    def hit(self, r: Ray, interval: Interval) -> Optional[HitRecord]:
        assert False, "Calling abstract"

    def bounding_box(self) -> AABB:
        assert False, "Calling abstract"

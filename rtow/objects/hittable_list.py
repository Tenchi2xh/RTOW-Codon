from typing import List, Optional

from .. import Ray, Interval, AABB
from .hittable import Hittable, HitRecord


class HittableList(Hittable):
    objects: List[Hittable]
    bbox: AABB

    def __init__(self, objects: List[Hittable] = []):
        self.objects = []
        self.bbox = AABB()
        for hittable in objects:
            self.add(hittable)

    def clear(self):
        self.objects = []

    def add(self, object: Hittable):
        self.objects.append(object)
        self.bbox = AABB.from_aabbs(self.bbox, object.bounding_box())

    def bounding_box(self) -> AABB:
        return self.bbox

    def hit(self, r: Ray, interval: Interval) -> Optional[HitRecord]:
        rec: Optional[HitRecord] = None
        closest_so_far = interval.max

        for hittable in self.objects:
            candidate_rec = hittable.hit(r, Interval(interval.min, closest_so_far))
            if candidate_rec:
                closest_so_far = candidate_rec.hit.t
                rec = candidate_rec

        return rec

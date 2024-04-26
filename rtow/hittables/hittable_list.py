from typing import List, Optional

from .. import Ray, Interval, Hittable, HitMat, AABB


class HittableList(Hittable):
    hittables: List[Hittable]
    bbox: AABB

    def __init__(self, hittables: List[Hittable] = []):
        self.hittables = []
        self.bbox = AABB()
        for hittable in hittables:
            self.add(hittable)

    def clear(self):
        self.hittables = []

    def add(self, hittable: Hittable):
        self.hittables.append(hittable)
        self.bbox = AABB.from_aabbs(self.bbox, hittable.bounding_box())

    def bounding_box(self) -> AABB:
        return self.bbox

    def hit(self, r: Ray, interval: Interval) -> Optional[HitMat]:
        hit: Optional[HitMat] = None
        closest_so_far = interval.max

        for hittable in self.hittables:
            candidate_hit = hittable.hit(r, Interval(interval.min, closest_so_far))
            if candidate_hit:
                closest_so_far = candidate_hit.hit.t
                hit = candidate_hit

        return hit

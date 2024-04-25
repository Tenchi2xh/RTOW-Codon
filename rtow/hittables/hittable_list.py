from typing import List, Optional

from .hittable import Hittable, Hit
from .. import Ray, Interval


class HittableList(Hittable):
    hittables: List[Hittable]

    def __init__(self):
        self.hittables = []

    def __init__(self, hittables: List[Hittable]):
        self.hittables = hittables

    def clear(self):
        self.hittables = []

    def add(self, hittable: Hittable):
        self.hittables.append(hittable)

    def hit(self, r: Ray, interval: Interval) -> Optional[Hit]:
        hit: Optional[Hit] = None
        closest_so_far = interval.max

        for hittable in self.hittables:
            candidate_hit = hittable.hit(r, Interval(interval.min, closest_so_far))
            if candidate_hit:
                closest_so_far = candidate_hit.t
                hit = candidate_hit

        return hit

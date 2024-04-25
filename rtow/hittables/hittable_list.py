from typing import List, Optional, Tuple

from .. import Ray, Interval, Hittable, Hit, Material


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

    def hit(self, r: Ray, interval: Interval) -> Optional[Tuple[Hit, Material]]:
        hit: Optional[Tuple[Hit, Material]] = None
        closest_so_far = interval.max

        for hittable in self.hittables:
            candidate_hit = hittable.hit(r, Interval(interval.min, closest_so_far))
            if candidate_hit:
                closest_so_far = candidate_hit[0].t
                hit = candidate_hit

        return hit

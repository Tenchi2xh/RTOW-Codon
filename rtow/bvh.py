from typing import Callable, List, Optional

from .aabb import AABB, empty
from .interval import Interval
from .ray import Ray
from .objects import HitRecord, Hittable, HittableList


class BVHNode(Hittable):
    left: Hittable
    right: Hittable
    bbox: AABB
    depth: int

    def __init__(self, left: Hittable, right: Hittable, bbox: AABB, depth: int):
        self.left = left
        self.right = right
        self.bbox = bbox
        self.depth = depth

    @staticmethod
    def from_list(list: HittableList):
        return BVHNode.make_node(list.objects, 0, len(list.objects), 0)

    @staticmethod
    def make_node(objects: List[Hittable], start: int, end: int, depth: int):

        # Build the bounding box of the span of source objects
        bbox = empty
        for i in range(start, end):
            bbox = AABB.from_aabbs(bbox, objects[i].bounding_box())

        axis = bbox.longest_axis()
        sort_key: Callable[[Hittable], float] = lambda a: -a.bounding_box().axis_interval(axis).min

        object_span = end - start

        if object_span == 1:
            left = right = objects[start]
        elif object_span == 2:
            left = objects[start]
            right = objects[start + 1]
        else:
            objects[start:end] = sorted(objects[start:end], key=sort_key)
            mid = start + object_span // 2
            left = BVHNode.make_node(objects, start, mid, depth + 1)
            right = BVHNode.make_node(objects, mid, end, depth + 1)

        return BVHNode(left, right, bbox, depth)


    def hit(self, r: Ray, ray_t: Interval) -> Optional[HitRecord]:
        if not self.bbox.hit(r, ray_t):
            return None
        else:
            hit_left = self.left.hit(r, ray_t)
            if hit_left:
                hit_right = self.right.hit(r, Interval(ray_t.min, hit_left.hit.t))
            else:
                hit_right = self.right.hit(r, ray_t)

            if hit_left and hit_right:
                return hit_left if hit_left.hit.t < hit_right.hit.t else hit_right

            return hit_left if hit_left else hit_right

    def bounding_box(self) -> AABB:
        return self.bbox

    def __repr__(self):
        sp0 = " " * 4 * (self.depth + 1)
        sp1 = " " * 4 * self.depth
        props = [
            f"{sp0}left={self.left},",
            f"{sp0}right={self.right},",
            f"{sp0}depth={self.depth}",
            f"{sp1})",
        ]
        return "BVHNode(" + "\n" + "\n".join(props)

from textwrap import dedent, indent
from random import randint
from typing import Callable, List, Optional

from .aabb import AABB
from .interval import Interval
from .ray import Ray
from .types import HitMat, Hittable
from .hittables.hittable_list import HittableList


class BVHNode(Hittable):
    left: Hittable
    right: Hittable
    bbox: AABB
    depth: int

    def __init__(self, left: Hittable, right: Hittable, depth: int):
        self.left = left
        self.right = right
        self.bbox = AABB.from_aabbs(left.bounding_box(), right.bounding_box())
        self.depth = depth

    @staticmethod
    def from_list(list: HittableList):
        return BVHNode.make_node(list.objects, 0, len(list.objects), 0)

    @staticmethod
    def make_node(objects: List[Hittable], start: int, end: int, depth: int):
        axis = randint(0, 2)

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

        return BVHNode(left, right, depth)


    def hit(self, r: Ray, ray_t: Interval) -> Optional[HitMat]:
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

            return hit_left or hit_right

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

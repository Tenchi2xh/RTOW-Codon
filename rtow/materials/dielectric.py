from math import sqrt
from random import random
from typing import Optional

from .. import Ray, Color, Material, Scatter, Hit, Vec3


def reflectance(cosine: float, refractive_index: float):
    # Use Schlick's approximation for reflectance
    r0 = (1 - refractive_index) / (1 + refractive_index)
    r0 = r0 * r0
    return r0 + (1 - r0) * pow((1 - cosine), 5)


class Dielectric(Material):
    # Refractive index in vacuum or air, or the ratio of the material's refractive index over
    # the refractive index of the enclosing media
    refractive_index: float

    def __init__(self, refractive_index: float):
        self.refractive_index = refractive_index

    def scatter(self, r_in: Ray, hit: Hit) -> Optional[Scatter]:
        index_ratio = (1.0 / self.refractive_index) if hit.front_face else self.refractive_index

        unit_direction = r_in.dir.unit()
        cos_theta = min(-unit_direction.dot(hit.normal), 1.0)
        sin_theta = sqrt(1.0 - cos_theta * cos_theta)

        cannot_refract = index_ratio * sin_theta > 1.0

        if cannot_refract or reflectance(cos_theta, index_ratio) > random():
            direction = unit_direction.reflect(hit.normal)
        else:
            direction = unit_direction.refract(hit.normal, index_ratio)

        return Scatter(
            scattered=Ray(hit.p, direction),
            attenuation=Color(1.0, 1.0, 1.0),
        )

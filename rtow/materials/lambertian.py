from typing import Optional


from .. import Ray, Color, Vec3
from ..objects import Hit
from ..textures import Texture, SolidColor
from ..color import black
from .material import Material, Scatter


class Lambertian(Material):
    texture: Texture

    def __init__(self, texture: Texture):
        self.texture = texture

    @staticmethod
    def from_color(albedo: Color = black):
        return Lambertian(SolidColor(albedo))

    def scatter(self, r_in: Ray, hit: Hit) -> Optional[Scatter]:
        scatter_direction = hit.normal + Vec3.random_unit()

        # Catch degenerate scatter direction: rare case when the random direction
        # is exactly opposite of the normal, which results in a zero length vector
        if scatter_direction.near_zero():
            scatter_direction = hit.normal

        return Scatter(
            scattered=Ray(hit.p, scatter_direction, r_in.time),
            attenuation=self.texture.value(hit.u, hit.v, hit.p),
        )

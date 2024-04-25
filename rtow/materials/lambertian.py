from typing import Optional

from .. import Ray, Color, Vec3, Material, Scatter, Hit


class Lambertian(Material):
    albedo: Color

    def __init__(self, albedo: Color = Color(0, 0, 0)):
        self.albedo = albedo

    def scatter(self, _: Ray, hit: Hit) -> Optional[Scatter]:
        scatter_direction = hit.normal + Vec3.random_unit()

        # Catch degenerate scatter direction: rare case when the random direction
        # is exactly opposite of the normal, which results in a zero length vector
        if scatter_direction.near_zero():
            scatter_direction = hit.normal

        return Scatter(
            scattered=Ray(hit.p, scatter_direction),
            attenuation=self.albedo,
        )

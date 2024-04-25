from typing import Optional

from .. import Ray, Color, Material, Scatter, Hit, Vec3


class Metal(Material):
    albedo: Color
    fuzz: float

    def __init__(self, albedo: Color = Color(0, 0, 0), fuzz: float = 0.0):
        self.albedo = albedo
        self.fuzz = fuzz

    def scatter(self, r_in: Ray, hit: Hit) -> Optional[Scatter]:
        reflected = r_in.dir.reflect(hit.normal).unit()
        reflected += self.fuzz * Vec3.random_unit()

        if reflected.dot(hit.normal) <= 0:
            return None

        return Scatter(
            scattered=Ray(hit.p, reflected),
            attenuation=self.albedo,
        )

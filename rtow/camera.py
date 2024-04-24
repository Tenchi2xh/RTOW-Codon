from typing import Optional

from .buffer import Buffer
from .interval import Interval
from .hittable import Hit, Hittable
from .ray import Ray
from .vec3 import Color, Point3, Vec3


class Camera:
    aspect_ratio: float  # Ratio of image width over height
    image_width: int     # Rendered image width in pixel count
    image_height: int    # Rendered image height
    center: Point3       # Camera center
    pixel00_loc: Point3  # Location of pixel 0, 0
    pixel_delta_u: Vec3  # Offset to pixel to the right
    pixel_delta_v: Vec3  # Offset to pixel below

    #             Δu           ---> viewport_u
    #      Q     |--|
    #       +---------------------+
    #       | .  .  .  .  .  .  . |  ---
    #       | .  .  .  .  .  .  . |   |  Δv
    #       | .  .  .  .  .  .  . |  ---
    #   |   | .  .  .  .  .  .  . |
    #   |   | .  .  .  .  .  .  . |
    #   v   +---------------------+
    #   viewport_v

    def __init__(self, aspect_ratio: float, image_width: int):
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width

        self.image_height = max(1, int(image_width / aspect_ratio))
        real_aspect_ratio = image_width / self.image_height

        self.center = Point3(0, 0, 0)

        # Determine viewport dimensions
        focal_length = 1.0
        viewport_height = 2.0
        viewport_width = viewport_height * real_aspect_ratio

        # Calculate the vectors across the horizontal and down the vertical viewport edges
        viewport_u = Vec3(viewport_width, 0, 0)
        viewport_v = Vec3(0, -viewport_height, 0)

        # Calculate the horizontal and vertical delta vectors from pixel to pixel
        self.pixel_delta_u = viewport_u / self.image_width
        self.pixel_delta_v = viewport_v / self.image_height

        # Calculate the location of the upper left pixel.
        viewport_upper_left = self.center - Vec3(0, 0, focal_length) - viewport_u / 2 - viewport_v / 2
        self.pixel00_loc = viewport_upper_left + 0.5 * (self.pixel_delta_u + self. pixel_delta_v)

    def ray_color(self, r: Ray, world: Hittable) -> Color:
        hit: Optional[Hit] = world.hit(r, Interval(0, float("inf")))

        if hit:
            return 0.5 * (hit.normal + Color(1, 1, 1))

        unit_direction = r.dir.unit()
        a = 0.5 * (unit_direction.y + 1.0)
        return (1.0 - a) * Color(1.0, 1.0, 1.0) + a * Color(0.5, 0.7, 1.0)

    def render(self, world: Hittable) -> Buffer:
        b = Buffer(self.image_width, self.image_height)

        #@par # type: ignore
        for j in range(self.image_height):
            row = []
            for i in range(self.image_width):
                pixel_center = self.pixel00_loc + (i * self.pixel_delta_u) + (j * self.pixel_delta_v)
                ray_direction = pixel_center - self.center
                r = Ray(self.center, ray_direction)

                pixel_color = self.ray_color(r, world)

                row.append(pixel_color)
            b[j] = row

        return b

from math import sqrt
from typing import Optional


from .ray import Ray
from .vec3 import Color, Point3, Vec3
from .interval import Interval
from .buffer import Buffer
from .hittable import Hit, Hittable
from .hittables import Sphere, HittableList


def ray_color(r: Ray, world: Hittable) -> Color:
    hit: Optional[Hit] = world.hit(r, Interval(0, float("inf")))

    if hit:
        return 0.5 * (hit.normal + Color(1, 1, 1))

    unit_direction = r.dir.unit()
    a = 0.5 * (unit_direction.y + 1.0)
    return (1.0 - a) * Color(1.0, 1.0, 1.0) + a * Color(0.5, 0.7, 1.0)


if __name__ == "__main__":
    # Image
    aspect_ratio = 16.0 / 9.0
    image_width = 400 * 2
    image_height = max(1, int(image_width / aspect_ratio))
    real_aspect_ratio = image_width / image_height

    # World
    world = HittableList()
    world.add(Sphere(Point3(0, 0, -1), 0.5))
    world.add(Sphere(Point3(0, -100.5, -1), 100))

    # Camera
    focal_length = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * real_aspect_ratio
    camera_center = Point3(0, 0, 0)

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

    # Calculate the vectors across the horizontal and down the vertical viewport edges
    viewport_u = Vec3(viewport_width, 0, 0)
    viewport_v = Vec3(0, -viewport_height, 0)

    # Calculate the horizontal and vertical delta vectors from pixel to pixel
    pixel_delta_u = viewport_u / image_width
    pixel_delta_v = viewport_v / image_height

    # Calculate the location of the upper left pixel.
    viewport_upper_left = camera_center - Vec3(0, 0, focal_length) - viewport_u / 2 - viewport_v / 2
    pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)

    with Buffer(image_width, image_height, "main", "ppm") as b:
        # @par
        for j in range(b.h):
            row = []
            for i in range(b.w):
                pixel_center = pixel00_loc + (i * pixel_delta_u) + (j * pixel_delta_v)
                ray_direction = pixel_center - camera_center
                r = Ray(camera_center, ray_direction)

                pixel_color = ray_color(r, world)

                row.append(pixel_color)
            b[j] = row

from typing import Optional

from .util import sample_square
from .buffer import Buffer
from .interval import Interval
from .types import Hit, Hittable
from .ray import Ray
from .vec3 import Color, Point3, Vec3


class Camera:
    aspect_ratio: float         # Ratio of image width over height
    image_width: int            # Rendered image width in pixel count
    image_height: int           # Rendered image height
    center: Point3              # Camera center
    pixel00_loc: Point3         # Location of pixel 0, 0
    pixel_delta_u: Vec3         # Offset to pixel to the right
    pixel_delta_v: Vec3         # Offset to pixel below
    samples_per_pixel: int      # Count of random samples for each pixel (antialiasing)
    pixel_samples_scale: float  # Color scale factor for a sum of pixel samples
    max_depth: int              # Maximum number of ray bounces into scene

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

    def __init__(
            self,
            aspect_ratio: float = 1.0,
            image_width: int = 100,
            samples_per_pixel: int = 10,
            max_depth: int = 10,
        ):
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
        self.samples_per_pixel = samples_per_pixel

        self.image_height = max(1, int(image_width / aspect_ratio))
        real_aspect_ratio = image_width / self.image_height
        self.pixel_samples_scale = 1.0 / samples_per_pixel

        self.center = Point3(0, 0, 0)
        self.max_depth = max_depth

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

    def ray_color(self, r: Ray, depth: int, world: Hittable) -> Color:
        # If we've exceeded the ray bounce limit, no more light is gathered
        if depth <= 0:
            return Color(0, 0, 0)

        # Min distance is 0.001 to avoid floating point precision errors
        # That way if the ray starts just below a surface,
        # that surface will be ignored and the ray can escape
        hit_mat = world.hit(r, Interval(0.001, float("inf")))

        # TODO: Flag to ignore materials and show normals
        # if hit:
        #     return 0.5 * (hit.normal + Color(1, 1, 1))

        if hit_mat:
            scatter = hit_mat.mat.scatter(r, hit_mat.hit)
            if scatter:
                return scatter.attenuation * self.ray_color(scatter.scattered, depth - 1, world)
            return Color(0, 0, 0)

        # Sky
        unit_direction = r.dir.unit()
        a = 0.5 * (unit_direction.y + 1.0)
        return (1.0 - a) * Color(1.0, 1.0, 1.0) + a * Color(0.5, 0.7, 1.0)

    def render(self, world: Hittable) -> Buffer:
        b = Buffer(self.image_width, self.image_height)

        for j in range(self.image_height):
            row = []
            for i in range(self.image_width):
                pixel_color = Color(0, 0, 0)
                for _ in range(self.samples_per_pixel):
                    r = self.get_ray(i, j)
                    pixel_color += self.ray_color(r, self.max_depth, world)

                row.append(self.pixel_samples_scale * pixel_color)
            b[j] = row

        return b

    def get_ray(self, i: int, j: int) -> Ray:
        """
        Constructs a camera ray originating from the origin and directed at randomly sampled
        point around the pixel location i, j
        """

        offset = sample_square()
        pixel_sample = (
            self.pixel00_loc +
            ((i + offset.x) * self.pixel_delta_u) +
            ((j + offset.y) * self.pixel_delta_v)
        )

        return Ray(self.center, pixel_sample - self.center)

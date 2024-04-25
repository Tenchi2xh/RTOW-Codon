from math import tan
from threading import Lock, get_ident
from typing import List, Tuple

from .chunks import CoordChunk, create_coordinate_chunks
from .util import degrees_to_radians, sample_square
from .buffer import Buffer
from .interval import Interval
from .types import Hit, Hittable
from .ray import Ray
from .vec3 import Color, Point3, Vec3


class Camera:
    image_width: int            # Rendered image width in pixel count
    image_height: int           # Rendered image height
    center: Point3              # Camera center
    pixel00_loc: Point3         # Location of pixel 0, 0
    pixel_delta_u: Vec3         # Offset to pixel to the right
    pixel_delta_v: Vec3         # Offset to pixel below
    samples_per_pixel: int      # Count of random samples for each pixel (antialiasing)
    pixel_samples_scale: float  # Color scale factor for a sum of pixel samples
    max_depth: int              # Maximum number of ray bounces into scene
    u: Vec3                     # Camera frame basis vectors
    v: Vec3                     #
    w: Vec3                     #
    chunk_size: int             # Size of chunks for each thread

    lock = Lock()

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
            aspect_ratio: float = 1.0,           # Ratio of image width over height
            image_width: int = 100,              # Rendered image width in pixel count
            samples_per_pixel: int = 10,         # Count of random samples for each pixel (antialiasing)
            max_depth: int = 10,                 # Maximum number of ray bounces into scene
            vfov: float = 90,                    # Vertical view angle (field of view)
            lookfrom: Point3 = Point3(0, 0, 0),  # Point camera is looking from
            lookat: Point3 = Point3(0, 0, -1),   # Point camera is looking at
            vup: Vec3 = Vec3(0, 1, 0),           # Camera-relative "up" direction
            chunk_size: int = 32,                # Size of chunks for each thread
        ):
        self.image_width = image_width
        self.samples_per_pixel = samples_per_pixel

        self.image_height = max(1, int(image_width / aspect_ratio))
        real_aspect_ratio = image_width / self.image_height
        self.pixel_samples_scale = 1.0 / samples_per_pixel

        self.center = lookfrom
        self.max_depth = max_depth

        self.chunk_size = chunk_size

        # Determine viewport dimensions
        focal_length = (lookfrom - lookat).length()
        theta = degrees_to_radians(vfov)
        h = tan(theta / 2)
        viewport_height = 2 * h * focal_length
        viewport_width = viewport_height * real_aspect_ratio

        # Calculate the u,v,w unit basis vectors for the camera coordinate frame.
        self.w = (lookfrom - lookat).unit()
        self.u = vup.cross(self.w).unit()
        self.v = self.w.cross(self.u)

        # Calculate the vectors across the horizontal and down the vertical viewport edges
        viewport_u = viewport_width * self.u    # Vector across viewport horizontal edge
        viewport_v = viewport_height * -self.v  # Vector down viewport vertical edge

        # Calculate the horizontal and vertical delta vectors from pixel to pixel
        self.pixel_delta_u = viewport_u / self.image_width
        self.pixel_delta_v = viewport_v / self.image_height

        # Calculate the location of the upper left pixel.
        viewport_upper_left = self.center - (focal_length * self.w) - viewport_u / 2 - viewport_v / 2
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

        coords_chunks = create_coordinate_chunks(self.image_width, self.image_height, self.chunk_size)

        def calculate_pixel(i: int, j: int) -> Color:
            pixel_color = Color(0, 0, 0)
            for _ in range(self.samples_per_pixel):
                r = self.get_ray(i, j)
                pixel_color += self.ray_color(r, self.max_depth, world)
            return self.pixel_samples_scale * pixel_color

        color_chunks = []

        # @par(chunk_size=1)
        for coords in coords_chunks:
            colors = [
                [calculate_pixel(i + coords.x0, j + coords.y0) for i in range(coords.width)]
                for j in range(coords.height)
            ]
            with self.lock:
                color_chunks.append((coords, colors))

        # Reassemble picture
        for chunk in color_chunks:
            coords, colors = chunk
            for j in range(len(colors)):
                for i in range(len(colors[j])):
                    b[i + coords.x0, j + coords.y0] = colors[j][i]

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

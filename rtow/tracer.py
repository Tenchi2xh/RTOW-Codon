from functools import partial
from random import random, shuffle
import sys
from math import ceil, tan
from threading import Lock
# <python-only>
from multiprocessing import Pool, Lock, Value
# </python-only>

from .chunks import CoordChunk, create_coordinate_chunks
from .util import degrees_to_radians, sample_square, p_inf
from .buffer import Buffer
from .interval import Interval
from .objects import Hittable, HittableList
from .ray import Ray
from .vec3 import Color, Point3, Vec3
from .bvh import BVHNode
from .camera import Camera


# <python-only>
chunks_done = Value("d", 0)
# </python-only>

class Tracer:
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
    focus_dist: float           # Distance from camera lookfrom point to plane of perfect focus
    defocus_angle: float        # Variation angle of rays through each pixel
    defocus_disk_u: Vec3        # Defocus disk horizontal radius
    defocus_disk_v: Vec3        # Defocus disk vertical radius
    render_mode: str            # "full" | "normals"
    camera_mode: str            # "perspective" | "orthographic"
    chunk_size: int             # Size of chunks for each thread
    num_threads: int            # Number of threads
    chunks_done: int            # For tracking progress
    num_chunks: int             # For tracking progress

    lock = Lock()

    def __init__(
            self,
            camera: Camera,
            aspect_ratio: float = 1.0,
            image_width: int = 100,
            samples_per_pixel: int = 10,
            max_depth: int = 10,
            render_mode: str = "full",
            chunk_size: int = 32,
            num_threads: int = 6,
        ):
        self.image_width = image_width
        self.samples_per_pixel = samples_per_pixel
        self.render_mode = render_mode
        self.camera_mode = camera.mode

        self.image_height = max(1, int(image_width / aspect_ratio))
        real_aspect_ratio = image_width / self.image_height
        self.pixel_samples_scale = 1.0 / samples_per_pixel

        self.chunk_size = chunk_size
        self.num_threads = num_threads

        self.center = camera.lookfrom
        self.focus_dist = camera.focus_dist
        self.max_depth = max_depth

        self.defocus_angle = camera.defocus_angle

        # Determine viewport dimensions
        theta = degrees_to_radians(camera.vfov)
        h = tan(theta / 2)
        viewport_height = 2 * h * camera.focus_dist
        viewport_width = viewport_height * real_aspect_ratio

        # Calculate the u,v,w unit basis vectors for the camera coordinate frame
        self.w = (camera.lookfrom - camera.lookat).unit()
        self.u = camera.vup.cross(self.w).unit()
        self.v = self.w.cross(self.u)

        # Calculate the vectors across the horizontal and down the vertical viewport edges
        viewport_u = viewport_width * self.u    # Vector across viewport horizontal edge
        viewport_v = viewport_height * -self.v  # Vector down viewport vertical edge

        # Calculate the horizontal and vertical delta vectors from pixel to pixel
        self.pixel_delta_u = viewport_u / self.image_width
        self.pixel_delta_v = viewport_v / self.image_height

        # Calculate the location of the upper left pixel
        viewport_upper_left = self.center - (camera.focus_dist * self.w) - viewport_u / 2 - viewport_v / 2
        self.pixel00_loc = viewport_upper_left + 0.5 * (self.pixel_delta_u + self. pixel_delta_v)

        # Calculate the camera defocus disk basis vectors
        defocus_radius = camera.focus_dist * tan(degrees_to_radians(camera.defocus_angle / 2))
        self.defocus_disk_u = self.u * defocus_radius
        self.defocus_disk_v = self.v * defocus_radius

    def ray_color(self, r: Ray, depth: int, world: Hittable) -> Color:
        # If we've exceeded the ray bounce limit, no more light is gathered
        if depth <= 0:
            return Color(0, 0, 0)

        # Min distance is 0.001 to avoid floating point precision errors
        # That way if the ray starts just below a surface,
        # that surface will be ignored and the ray can escape
        rec = world.hit(r, Interval(0.001, p_inf))

        if rec:
            if self.render_mode == "normals":
                return 0.5 * (rec.hit.normal + Color(1, 1, 1))

            scatter = rec.mat.scatter(r, rec.hit)
            if scatter:
                return scatter.attenuation * self.ray_color(scatter.scattered, depth - 1, world)
            return Color(0, 0, 0)

        # Sky
        unit_direction = r.direction.unit()
        a = 0.5 * (unit_direction.y + 1.0)
        return (1.0 - a) * Color(1.0, 1.0, 1.0) + a * Color(0.5, 0.7, 1.0)

    def report(self, bvh_depth: int, num_chunks: int):
        res1 = f"{self.image_width} x {self.image_height}"
        res2 = f"{self.image_width * self.image_height / 1e6:3.1f}MP"
        bvh_info1 = f"{bvh_depth}"
        bvh_info2 = f"{2**(bvh_depth + 1)} leaves"
        chunks =  f"{num_chunks} x {self.chunk_size} x {self.chunk_size}"
        print(f"Resolution:        {res1:>14} = {res2}")
        print(f"BVH tree depth:    {bvh_info1:>14} = {bvh_info2}")
        print(f"Samples per pixel: {self.samples_per_pixel:14d} @ {self.max_depth} bounces")
        print(f"Chunks:            {chunks:>14} @ {self.num_threads} threads")
        print(f"Mode:              {self.render_mode:>14}")
        print()
        self.chunks_done = 0
        # <python-only>
        chunks_done.value = 0
        # </python-only>
        self.num_chunks = num_chunks

    def status(self):
        i = self.chunks_done
        # <python-only>
        i = int(chunks_done.value)
        # </python-only>
        max = self.num_chunks
        c = str(i).rjust(len(str(max)))
        p = i / float(max)
        pp = "100" if i == max else f"{100 * p:4.1f}"
        b0 = "#" * int(p * 20)
        b1 = "-" * (20 - len(b0))
        print(f"\rRendering chunks: [{b0}{b1}] {c} / {max} ({pp}%) ", end="", flush=True, file=sys.stderr)

        self.chunks_done += 1
        # <python-only>
        with chunks_done.get_lock():
            chunks_done.value += 1
        # </python-only>

    def render(self, world: HittableList) -> Buffer:
        b = Buffer(self.image_width, self.image_height)
        bvh, depth = BVHNode.from_list(world)

        coords_chunks = create_coordinate_chunks(self.image_width, self.image_height, self.chunk_size)
        # <python-only>
        shuffle(coords_chunks)
        # </python-only>

        color_chunks = []

        def calculate_pixel(i: int, j: int) -> Color:
            pixel_color = Color(0, 0, 0)
            for _ in range(self.samples_per_pixel):
                r = self.get_ray(i, j)
                pixel_color += self.ray_color(r, self.max_depth, bvh)
            return self.pixel_samples_scale * pixel_color

        # Creating threads is super slow so we only want to create them once
        chunks_per_thread = ceil(len(coords_chunks) / self.num_threads)

        self.report(depth, len(coords_chunks))
        self.status()

        # <python-only>
        func = partial(calculate_coord_chunk, self, bvh)
        with Pool(processes=self.num_threads) as pool:
            color_chunks = pool.map(func, coords_chunks, chunksize=chunks_per_thread)
        # </python-only>

        # <codon-only>
        @par(num_threads=self.num_threads, chunk_size=chunks_per_thread, ordered=False, schedule="static")
        for coords in coords_chunks:
            colors = [
                [calculate_pixel(i + coords.x0, j + coords.y0) for i in range(coords.width)]
                for j in range(coords.height)
            ]
            with self.lock:
                color_chunks.append((coords, colors))
                self.status()
        # </codon-only>

        # Reassemble picture
        for chunk in color_chunks:
            coords, colors = chunk
            for j in range(len(colors)):
                for i in range(len(colors[j])):
                    b[i + coords.x0, j + coords.y0] = colors[j][i]

        print(file=sys.stderr)
        return b

    def get_ray(self, i: int, j: int) -> Ray:
        """
        Construct a camera ray originating from the defocus disk and directed at a randomly
        sampled point around the pixel location i, j.
        """

        offset = sample_square()
        pixel_sample = (
            self.pixel00_loc +
            ((i + offset.x) * self.pixel_delta_u) +
            ((j + offset.y) * self.pixel_delta_v)
        )

        if self.camera_mode == "perspective":
            ray_origin = self.center
        else:
            # Not in book: orthographic camera
            # Rays are all parallel to the -w direction instead of coming from a single point
            # Imagine another focal plane but where the camera is, with the same size as the focal plane
            ray_origin = pixel_sample + (self.w * self.focus_dist)

        if self.defocus_angle > 0:
            ray_origin += self.defocus_disk_sample()

        ray_direction = pixel_sample - ray_origin

        ray_time = random()

        return Ray(
            orig=ray_origin,
            dir=ray_direction,
            time=ray_time,
        )

    def defocus_disk_sample(self):
        """Returns a random point in the camera defocus disk."""
        p = Vec3.random_in_unit_disk()
        return (p.x * self.defocus_disk_u) + (p.y * self.defocus_disk_v)


# <python-only>
def calculate_coord_chunk(tracer: Tracer, bvh: BVHNode, coords: CoordChunk):
    def calculate_pixel(i, j):
        pixel_color = Color(0, 0, 0)
        for _ in range(tracer.samples_per_pixel):
            r = tracer.get_ray(i, j)
            pixel_color += tracer.ray_color(r, tracer.max_depth, bvh)
        return tracer.pixel_samples_scale * pixel_color

    colors = [
        [calculate_pixel(i + coords.x0, j + coords.y0) for i in range(coords.width)]
        for j in range(coords.height)
    ]

    with tracer.lock:
        tracer.status()

    return coords, colors
# </python-only>

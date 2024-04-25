from math import sqrt
from typing import Optional

from .camera import Camera
from .vec3 import Point3
from .hittables import Sphere, HittableList


if __name__ == "__main__":
    world = HittableList()

    world.add(Sphere(Point3(0, 0, -1), 0.5))
    world.add(Sphere(Point3(0, -100.5, -1), 100))

    camera = Camera(
        aspect_ratio=16.0 / 9.0,
        image_width=1280,
        samples_per_pixel=10,
    )

    buffer = camera.render(world)
    buffer.save_ppm("main")

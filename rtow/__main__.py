from .camera import Camera
from .vec3 import Point3, Color
from .hittables import Sphere, HittableList
from .materials import Lambertian


if __name__ == "__main__":
    world = HittableList()

    matte_gray = Lambertian(Color(0.5, 0.5, 0.5))
    matte_red = Lambertian(Color(0.5, 0.0, 0.0))

    world.add(Sphere(Point3(0, 0, -1), 0.5, matte_gray))
    world.add(Sphere(Point3(0, -100.5, -1), 100, matte_red))

    camera = Camera(
        aspect_ratio=16.0 / 9.0,
        image_width=400,
        samples_per_pixel=100,
        max_depth=50,
    )

    buffer = camera.render(world)
    buffer.save_ppm("main")

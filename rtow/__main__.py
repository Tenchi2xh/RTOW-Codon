from math import cos, pi
from .camera import Camera
from .vec3 import Vec3, Point3, Color
from .hittables import Sphere, HittableList
from .materials import Lambertian, Metal, Dielectric


def world1():
    world = HittableList()

    material_ground = Lambertian(Color(0.8, 0.8, 0.0))
    material_center = Lambertian(Color(0.1, 0.2, 0.5))
    material_left   = Dielectric(1.50)
    material_bubble = Dielectric(1.00 / 1.50)
    material_right  = Metal(Color(0.8, 0.6, 0.2), fuzz=1.0)

    world.add(Sphere(Point3( 0.0, -100.5, -1.0), 100.0, material_ground))
    world.add(Sphere(Point3( 0.0,    0.0, -1.2),   0.5, material_center))
    world.add(Sphere(Point3(-1.0,    0.0, -1.0),   0.5, material_left))
    world.add(Sphere(Point3(-1.0,    0.0, -1.0),   0.4, material_bubble))
    world.add(Sphere(Point3( 1.0,    0.0, -1.0),   0.5, material_right))

    return world


def world2():
    world = HittableList()
    R = cos(pi / 4)

    material_left  = Lambertian(Color(0, 0, 1))
    material_right = Lambertian(Color(1, 0, 0))

    world.add(Sphere(Point3(-R, 0, -1), R, material_left))
    world.add(Sphere(Point3( R, 0, -1), R, material_right))

    return world


if __name__ == "__main__":
    camera = Camera(
        aspect_ratio=16.0 / 9.0,
        image_width=400,
        samples_per_pixel=100,
        max_depth=50,
        vfov=20,
        lookfrom=Point3(-2, 2, 1),
        lookat=Point3(0, 0, -1),
        vup=Vec3(0, 1, 0),
    )

    buffer = camera.render(world1())
    buffer.save_ppm("main")

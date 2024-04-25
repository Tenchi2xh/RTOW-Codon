from .camera import Camera
from .vec3 import Point3, Color
from .hittables import Sphere, HittableList
from .materials import Lambertian, Metal


if __name__ == "__main__":
    world = HittableList()


    material_ground = Lambertian(Color(0.8, 0.8, 0.0))
    material_center = Lambertian(Color(0.1, 0.2, 0.5))
    material_left   = Metal(Color(0.8, 0.8, 0.8), fuzz=0.3)
    material_right  = Metal(Color(0.8, 0.6, 0.2), fuzz=1.0)


    world.add(Sphere(Point3( 0.0, -100.5, -1.0), 100.0, material_ground))
    world.add(Sphere(Point3( 0.0,    0.0, -1.2),   0.5, material_center))
    world.add(Sphere(Point3(-1.0,    0.0, -1.0),   0.5, material_left))
    world.add(Sphere(Point3( 1.0,    0.0, -1.0),   0.5, material_right))

    camera = Camera(
        aspect_ratio=16.0 / 9.0,
        image_width=400,
        samples_per_pixel=100,
        max_depth=50,
    )

    buffer = camera.render(world)
    buffer.save_ppm("main")

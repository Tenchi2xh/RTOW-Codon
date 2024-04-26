import os
from datetime import datetime
from math import cos, pi
from random import random, uniform

from .camera import Camera
from .vec3 import Vec3, Point3, Color
from .hittables import Sphere, HittableList
from .materials import Lambertian, Metal, Dielectric


if __name__ == "__main__":
    world = HittableList()

    ground_material = Lambertian(Color(0.5, 0.5, 0.5))
    world.add(Sphere(1000, ground_material, Point3(0, -1000, 0)))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random()
            center = Point3(a + 0.9 * random(), 0.2, b + 0.9 * random())

            if (center - Point3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    # diffuse
                    albedo = Color.random() * Color.random()
                    sphere_material = Lambertian(albedo)
                    center2 = center + Vec3(0, uniform(0, 0.5), 0)
                    world.add(Sphere(0.2, sphere_material, center, center2))
                elif choose_mat < 0.95:
                    # metal
                    albedo = Color.random(0.5, 1)
                    fuzz = uniform(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                    world.add(Sphere(0.2, sphere_material, center))
                else:
                    # glass
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(0.2, sphere_material, center))

    material1 = Dielectric(1.5)
    world.add(Sphere(1.0, material1, Point3(0, 1, 0)))

    material2 = Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(1.0, material2, Point3(-4, 1, 0)))

    material3 = Metal(Color(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(1.0, material3, Point3(4, 1, 0)))

    camera = Camera(
        aspect_ratio=16.0 / 9.0,
        image_width=400,
        samples_per_pixel=10,
        max_depth=5,

        vfov=20,
        lookfrom=Point3(13, 2, 3),
        lookat=Point3(0, 0, 0),
        vup=Vec3(0, 1, 0),

        defocus_angle=0.6,
        focus_dist=10.0,
    )

    buffer = camera.render(world)

    timestamp = datetime.now().isoformat()
    filename = f"{timestamp}_s{camera.samples_per_pixel}_d{camera.max_depth}"
    buffer.save_ppm(filename)

    try:
        os.system(f"imgcat -W 2400px renders/{filename}.ppm")
    except:
        pass

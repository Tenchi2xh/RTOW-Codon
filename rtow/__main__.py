import os
from datetime import datetime
from random import random, uniform

from .tracer import Tracer, Camera
from .vec3 import Vec3, Point3, Color
from .objects import Sphere, HittableList
from .materials import Lambertian, Metal, Dielectric
from .textures import Checker, ImageTexture, NoiseTexture


def bouncing_spheres():
    world = HittableList()

    checker = Checker.from_colors(0.32, Color(0.2, 0.3, 0.1), Color.all(0.9))
    world.add(Sphere(1000, Lambertian(checker), Point3(0, -1000, 0)))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random()
            center = Point3(a + 0.9 * random(), 0.2, b + 0.9 * random())

            if (center - Point3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    # diffuse
                    albedo = Color.random() * Color.random()
                    sphere_material = Lambertian.from_color(albedo)
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

    material2 = Lambertian.from_color(Color(0.4, 0.2, 0.1))
    world.add(Sphere(1.0, material2, Point3(-4, 1, 0)))

    material3 = Metal(Color(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(1.0, material3, Point3(4, 1, 0)))

    camera = Camera(
        vfov=20,
        lookfrom=Point3(13, 2, 3),
        lookat=Point3(0, 0, 0),
        vup=Vec3(0, 1, 0),

        defocus_angle=0.6,
        focus_dist=10.0,
    )

    return world, camera


def bouncing_spheres_ortho():
    world, camera = bouncing_spheres()
    camera.mode = "orthographic"
    return world, camera


def checkered_spheres():
    world = HittableList()

    checker = Checker.from_colors(0.32, Color(0.2, 0.3, 0.1), Color.all(0.9))

    world.add(Sphere(10, Lambertian(checker), Point3(0, -10, 0)))
    world.add(Sphere(10, Lambertian(checker), Point3(0,  10, 0)))

    camera = Camera(
        vfov=20,
        lookfrom=Point3(13, 2, 3),
        lookat=Point3(0, 0, 0),
        vup=Vec3(0, 1, 0),

        defocus_angle=0,
    )

    return world, camera


def earth():
    world = HittableList()

    earth_texture = ImageTexture("images/earthmap.jpg")
    earth_surface = Lambertian(earth_texture)
    globe = Sphere(2, earth_surface, Point3(0, 0, 0))

    world.add(globe)

    camera = Camera(
        vfov=20,
        lookfrom=Point3(0, 0, 12),
        lookat=Point3(0, 0, 0),
        vup=Vec3(0, 1, 0),

        defocus_angle=0,
    )

    return world, camera


def perlin_spheres():
    world = HittableList()

    perlin_texture = Lambertian(NoiseTexture(4))
    world.add(Sphere(1000, perlin_texture, Point3(0, -1000, 0)))
    world.add(Sphere(2, perlin_texture, Point3(0, 2, 0)))

    camera = Camera(
        vfov=20,
        lookfrom=Point3(13, 2, 3),
        lookat=Point3(0, 0, 0),
        vup=Vec3(0, 1, 0),

        defocus_angle=0,
    )

    return world, camera


if __name__ == "__main__":
    world, camera = (
        bouncing_spheres,
        bouncing_spheres_ortho,
        checkered_spheres,
        earth,
        perlin_spheres,
    )[0]()

    tracer = Tracer(
        camera=camera,
        aspect_ratio=16.0 / 9.0,
        image_width=400,
        samples_per_pixel=100,
        max_depth=50,
    )

    start = datetime.now()
    buffer = tracer.render(world)
    end = datetime.now()

    duration = (end - start).seconds
    timestamp = start.isoformat().replace("T", "-").replace(":", "").split(".")[0]
    filename = f"{timestamp}_ssp={tracer.samples_per_pixel}_md={tracer.max_depth}_t={duration}s"
    buffer.save_ppm(filename)

    try:
        print()
        os.system(f"imgcat -W 2400px renders/{filename}.ppm")
    except:
        pass

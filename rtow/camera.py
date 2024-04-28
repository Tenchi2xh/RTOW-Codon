from .vec3 import Point3, Vec3


class Camera:
    vfov: float           # Vertical view angle (field of view)
    lookfrom: Point3      # Point camera is looking from
    lookat: Point3        # Point camera is looking at
    vup: Vec3             # Camera-relative "up" direction
    defocus_angle: float  # Variation angle of rays through each pixel
    focus_dist: float     # Distance from camera lookfrom point to plane of perfect focus
    mode: str             # "perspective" | "orthographic"

    def __init__(
            self,
            vfov: float = 90,
            lookfrom: Point3 = Point3(0, 0, 0),
            lookat: Point3 = Point3(0, 0, -1),
            vup: Vec3 = Vec3(0, 1, 0),
            defocus_angle: float = 0,
            focus_dist: float = 10,
            mode: str = "perspective",
        ):
        self.vfov = vfov
        self.lookfrom = lookfrom
        self.lookat = lookat
        self.vup = vup
        self.defocus_angle = defocus_angle
        self.focus_dist = focus_dist
        self.mode = mode

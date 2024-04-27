from .. import Ray, Point3, Vec3

class Hit:
    p: Point3
    normal: Vec3
    t: float
    u: float
    v: float
    front_face: bool

    def __init__(self, p: Point3, outward_normal: Vec3, t: float, r: Ray):
        self.p = p
        self.t = t
        self.u = 0
        self.v = 0
        self.front_face = r.direction.dot(outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal

from math import pi
from random import random

from .vec3 import Vec3


def degrees_to_radians(degrees: float):
    return degrees * pi / 180.0


def sample_square() -> Vec3:
    """Returns the vector to a random point in the [-.5,-.5]-[+.5,+.5] unit square."""
    return Vec3(random() - 0.5, random() - 0.5, 0)

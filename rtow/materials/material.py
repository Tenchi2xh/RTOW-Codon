from typing import Optional

from .. import Ray, Color
from ..objects import Hit


class Scatter:
    attenuation: Color
    scattered: Ray

    def __init__(self, attenuation: Color, scattered: Ray):
        self.attenuation = attenuation
        self.scattered = scattered


class Material:
    def scatter(self, r_in: Ray, hit: Hit) -> Optional[Scatter]:
        assert False, "Calling abstract"

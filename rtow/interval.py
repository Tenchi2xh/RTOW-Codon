from .util import p_inf, m_inf

class Interval:
    min: float
    max: float

    def __init__(self, min: float = m_inf, max: float = p_inf):
        self.min = min
        self.max = max

    @staticmethod
    def from_intervals(a: Interval, b: Interval):
        """Create the interval tightly enclosing the two input intervals."""
        return Interval(
            min=a.min if a.min <= b.min else b.min,
            max=a.max if a.max >= b.max else b.max,
        )

    def size(self):
        return self.max - self.min

    def contains(self, x: float):
        return self.min <= x <= self.max
    
    def surrounds(self, x: float):
        return self.min < x < self.max
    
    def clamp(self, x: float):
        if x < self.min:
            return self.min
        elif x > self.max:
            return self.max
        return x

    def expand(self, delta: float):
        padding = delta / 2
        return Interval(self.min - padding, self.max + padding)


empty = Interval(p_inf, m_inf)
universe = Interval(m_inf, p_inf)

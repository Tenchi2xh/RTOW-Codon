from .util import p_inf, m_inf

class Interval:
    min: float
    max: float

    def __init__(self):
        self.min = m_inf
        self.max = p_inf

    def __init__(self, min: float, max: float):
        self.min = min
        self.max = max

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

empty = Interval(p_inf, m_inf)
universe = Interval(m_inf, p_inf)

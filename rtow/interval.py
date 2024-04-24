class Interval:
    min: float
    max: float

    def __init__(self):
        self.min = float("-inf")
        self.max = float("+inf")

    def __init__(self, min: float, max: float):
        self.min = min
        self.max = max

    def size(self):
        return self.max - self.min

    def contains(self, x: float):
        return self.min <= x <= self.max
    
    def surrounds(self, x: float):
        return self.min < x < self.max

empty = Interval(float("+inf"), float("-inf"))
universe = Interval(float("-inf"), float("+inf"))

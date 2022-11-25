import math


class RunningStats:
    default_spread: float = 0.0

    n: int
    old_mean: float
    new_mean: float
    old_spread: float
    new_spread: float

    def __init__(self) -> None:
        self.n = 0

    def add(self, value: float) -> None:
        if math.isnan(value) or math.isinf(value):
            raise ValueError("Bad value: " + value)
        self.n += 1

        if self.n == 1:
            self.old_mean = value
            self.new_mean = value
            self.old_spread = 0.0
            self.new_spread = 0.0
        else:
            self.new_mean = self.old_mean + (value - self.old_mean) / self.n
            self.new_spread = self.old_spread + (value - self.old_mean) * (value - self.new_mean)
            # setup for next iteration
            self.old_mean = self.new_mean
            self.old_spread = self.new_spread

    def get_num_samples(self) -> int:
        return self.n

    def get_mean(self) -> float:
        if self.n > 0:
            return self.new_mean
        return 0.0
    
    def get_variance(self) -> float:
        if self.n > 1:
            return self.new_spread / (self.n - 1)
        return RunningStats.default_spread

    def get_std_dev(self) -> float:
        return math.sqrt(self.get_variance())

    def get_EV_std_dev(self) -> float:
        if self.n > 0:
            return math.sqrt(self.get_variance()/self.get_num_samples())
        return RunningStats.default_spread

    def get_EV_variance(self) -> float:
        if self.n > 0:
            return self.get_variance()/self.get_num_samples()
        return RunningStats.default_spread

    def reset(self) -> None:
        self.n = 0
            
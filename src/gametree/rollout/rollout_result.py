from math import isinf, isnan
from typing import Dict


class RolloutResult:
    values: Dict
    total_prob: float

    def __init__(
        self,
        values: Dict,
        total_prob: float,
    ) -> None:
        if isnan(total_prob) or isinf(total_prob) or total_prob == 0:
            raise RuntimeError(f"Bad total probability{total_prob}")
        self.values = values
        self.total_prob = total_prob

    def get_mean(self) -> float:
        mean = 0
        for value, prob in self.values.items():
            mean += value*prob
        mean /= self.total_prob
        return mean

    def get_variance(self, mean: float, num_samples: int):
        var = 0
        for value, prob in self.values.items():
            diff = mean - value
            var += (diff**2)*prob
        var /= self.total_prob
        var *= num_samples/(num_samples - 1)
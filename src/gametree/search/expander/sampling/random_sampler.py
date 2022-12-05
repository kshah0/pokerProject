import random
from gametree.search.expander.sampling.stochastic_sampler import StochasticSampler


class RandomSampler(StochasticSampler):
    def __init__(self, num_bet_size_samples: int = 5) -> None:
        super().__init__(num_bet_size_samples)

    def get_stochastic_samples(self, n: int) -> List[float]:
        samples = []
        for i in range(n):
            samples.append(random.random())
        samples.sort()
        return samples
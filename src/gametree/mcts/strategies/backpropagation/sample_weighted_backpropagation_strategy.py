from mcts.nodes.decision_node import DecisionNode
from mcts.nodes.opponent_node import OpponentNode
from mcts.strategies.backpropagation.backpropagation_strategy import BackPropagationStrategy
from mcts.strategies.backpropagation.running_stats import RunningStats


class SampleWeightedBackpropStrat(BackPropagationStrategy):
    stats: RunningStats

    def __init__(self):
        self.stats = RunningStats()

    # @Override
    def get_EV(self) -> float:
        return self.stats.get_mean()

    # @Override
    def get_num_samples(self) -> int:
        return self.stats.get_num_samples()

    # @Override
    def get_std_dev(self) -> float:
        return self.stats.get_std_dev()

    # @Override
    def get_EV_std_dev(self) -> float:
        return self.stats.get_EV_std_dev()

    # @Override
    def get_variance(self) -> float:
        return self.stats.get_variance()

    # @Override
    def get_num_samples_in_mean(self) -> int:
        return self.stats.get_num_samples()

    # @Override
    def on_back_propagate(self, value: float) -> None:
        self.stats.add(value)

    class Factory(BackPropagationStrategy.Factory):
        # @Override
        def create_for_decision_node(self, node: DecisionNode) -> BackPropagationStrategy:
            return SampleWeightedBackpropStrat()

        # @Override
        def create_for_opponent_node(self, node: OpponentNode) -> BackPropagationStrategy:
            return SampleWeightedBackpropStrat()
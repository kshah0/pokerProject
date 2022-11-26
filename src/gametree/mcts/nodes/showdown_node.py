from abc import ABC, abstractmethod
from action.probability_action import ProbabilityAction
from gametree.gamestate.game_state import GameState
from mcts.nodes.inner_node import InnerNode
from mcts.nodes.leaf_node import LeafNode
from mcts.strategies.backpropagation.running_stats import RunningStats


class ShowdownNode(LeafNode, ABC):
    stats: RunningStats

    def __init__(self, parent: InnerNode, last_action: ProbabilityAction) -> None:
        super().__init__(parent, last_action)
        self.stats = RunningStats()
    
    # @Override
    def get_EV(self) -> float:
        return self.stats.get_mean()

    # @Override
    def get_std_dev(self) -> float:
        return self.stats.get_std_dev()

    # @Override
    def get_EV_std_dev(self) -> float:
        return self.stats.get_EV_std_dev()

    # @Override
    def get_num_samples_in_mean(self) -> int:
        return self.stats.get_num_samples()

    # @Override
    def get_variance(self) -> float:
        return self.stats.get_variance()
    
    # @Override
    def get_num_samples(self) -> int:
        return self.stats.get_num_samples()
    
    # @Override
    def get_EV_variance(self) -> float:
        return self.stats.get_EV_variance()

    # @Override
    def backpropagate(self, value: float) -> None:
        self.stats.add(value)
        self.parent.backpropagate(value)

    class Factory(ABC):

        @abstractmethod
        def create(
            self,
            game_state: GameState,
            parent: InnerNode,
            prob_action: ProbabilityAction,
        ) -> LeafNode:
            pass
            
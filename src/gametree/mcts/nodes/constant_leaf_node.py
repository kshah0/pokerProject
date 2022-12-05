from action.probability_action import ProbabilityAction
from mcts.nodes.inner_node import InnerNode
from mcts.nodes.leaf_node import LeafNode


class ConstantLeafNode(LeafNode):
    value: int
    num_samples: int

    def __init__(
        self, 
        parent: InnerNode,
        last_action: ProbabilityAction,
        value: int
    ) -> None:
        super().__init__(parent, last_action)
        self.value = value
        self.num_samples = 0
        self.game_state = self.parent.game_state

    # @Override
    def simulate(self) -> float:
        return self.value

    # @Override
    def backpropagate(self, value: float) -> None:
        self.num_samples += 1
        self.parent.backpropagate(value)

    # @Override
    def get_EV(self) -> float:
        return self.value

    # @Override
    def get_std_dev(self) -> float:
        return 0

    # @Override
    def get_EV_std_dev(self) -> float:
        return 0

    # @Override
    def get_num_samples_in_mean(self) -> int:
        return self.num_samples

    # @Override
    def get_variance(self) -> float:
        return 0
    
    # @Override
    def get_num_samples(self) -> int:
        return self.num_samples
    
    # @Override
    def get_EV_variance(self) -> float:
        return 0

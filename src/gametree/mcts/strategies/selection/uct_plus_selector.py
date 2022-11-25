import math
from mcts.nodes.inode import INode
from mcts.strategies.selection.max_function_selector import MaxFunctionSelector


class UCTPlusSelector(MaxFunctionSelector):
    C1: float
    C2: float

    def __init__(
        self,
        C1: float,
        C2: float,
    ) -> None:
        self.C1 = C1
        self.C2 = C2

    # @Override
    def evaluate(self, node: INode) -> float:
        num_samples = node.get_num_samples()
        if num_samples == 0:
            return 0
        num_parent_samples = node.parent.get_num_samples()
        std_dev = node.get_EV_std_dev()
        return (
            node.get_EV() + 
            self.C1*math.sqrt(math.log(num_parent_samples)/num_samples) +
            self.C2*std_dev
        )

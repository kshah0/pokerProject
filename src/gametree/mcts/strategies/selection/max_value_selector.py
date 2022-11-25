from mcts.nodes.inode import INode
from mcts.strategies.selection.max_function_selector import MaxFunctionSelector


class MaxValueSelector(MaxFunctionSelector):
    # @Override
    def evaluate(self, node: INode) -> float:
        return node.get_EV()
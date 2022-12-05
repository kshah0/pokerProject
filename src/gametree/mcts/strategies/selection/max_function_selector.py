from abc import ABC, abstractmethod
from mcts.nodes.inner_node import InnerNode
from mcts.nodes.inode import INode
from mcts.strategies.selection.max_value_selector import MaxValueSelector
from mcts.strategies.selection.selection_strategy import SelectionStrategy


class MaxFunctionSelector(SelectionStrategy, ABC):

    # @Override
    def select(self, inner_node: InnerNode) -> INode:
        children = inner_node.children
        max_node = None
        max_value = -999999999999999
        for child in children:
            value = self.evaluate(child)
            if value > max_value:
                max_value = value
                max_node = child
        if max_node is None:
            # fall back on max value selector which can't fail
            return MaxValueSelector().select(inner_node)
        return max_node

    @abstractmethod
    def evaluate(self, node: INode) -> float:
        pass
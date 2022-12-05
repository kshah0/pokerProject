from abc import ABC
from action.probability_action import ProbabilityAction
from mcts.nodes.inner_node import InnerNode
from mcts.nodes.inode import INode


class LeafNode(INode, ABC):

    # Inherited from INode
    # parent: InnerNode
    # game_state: GameState
    # last_action: ProbabilityAction

    def __init__(
        self,
        parent: InnerNode,
        last_action: ProbabilityAction,
    ) -> None:
        self.parent = parent
        self.last_action = last_action
    
    # @Override
    def select_recursively(self) -> INode:
        return self

    # @Override
    def expand(self) -> None:
        return
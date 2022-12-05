from abc import ABC, abstractmethod

from mcts.nodes.inner_node import InnerNode
from mcts.nodes.inode import INode


class SelectionStrategy(ABC):
    
    @abstractmethod
    def select(self, inner_node: InnerNode) -> INode:
        pass
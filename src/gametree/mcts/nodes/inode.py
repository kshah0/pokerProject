from abc import ABC, abstractmethod
from __future__ import annotations
from action.probability_action import ProbabilityAction

from mcts.game_state import GameState
from mcts.nodes.inner_node import InnerNode

class INode(ABC):
    parent: InnerNode
    last_action: ProbabilityAction
    game_state: GameState

    @abstractmethod
    def select_recursively(self) -> INode:
        pass

    @abstractmethod
    def expand(self) -> None:
        pass

    @abstractmethod
    def simulate(self) -> float:
        pass

    @abstractmethod
    def backpropagate(self, value: float) -> None:
        pass

    @abstractmethod
    def get_EV(self) -> float:
        pass

    @abstractmethod
    def get_std_dev(self) -> float:
        pass

    @abstractmethod
    def get_EV_std_dev(self) -> float:
        pass

    @abstractmethod
    def get_num_samples_in_mean(self) -> int:
        pass

    @abstractmethod
    def get_variance(self) -> float:
        pass
    
    @abstractmethod
    def get_num_samples(self) -> int:
        pass
    
    @abstractmethod
    def get_EV_variance(self) -> float:
        pass

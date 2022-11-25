from abc import ABC, abstractmethod
from __future__ import annotations

from mcts.nodes.decision_node import DecisionNode
from mcts.nodes.opponent_node import OpponentNode

class BackPropagationStrategy(ABC):

    @abstractmethod
    def on_back_propagate(self, value: float) -> None:
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

    class Factory(ABC):
        
        @abstractmethod
        def create_for_decision_node(self, node: DecisionNode) -> BackPropagationStrategy:
            pass
        
        @abstractmethod
        def create_for_opponent_node(self, node: OpponentNode) -> BackPropagationStrategy:
            pass
from abc import ABC, abstractmethod
from typing import Tuple, List
from gametree.playerstate.player_id import PlayerId

from __future__ import annotations

from gametree.gamestate.game_state import GameState
from gametree.mcts.nodes.inode import INode

class OpponentModel(ABC):

    @abstractmethod
    def get_check_bet_probabilities(self, gamestate:GameState, actor:PlayerId) -> Tuple[float,float]:
        pass

    @abstractmethod
    def get_fold_call_raise_probabilities(self, gamestate:GameState, actor:PlayerId) -> Tuple[float, float, float]:
        pass

    @abstractmethod
    def get_bot_id(self) -> PlayerId:
        pass

    # May not need these functions below
    def get_showdown_probabilities(self, gamestate:GameState, actor:PlayerId) -> List[float]:
        pass

    def set_chosen_node(self, node:INode) -> None:
        pass

    def get_chosen_node(self) -> INode:
        pass

    def assume_permanently(self, gamestate:GameState) -> None:
        pass

    def assume_temporarily(self, gamestate:GameState) -> None:
        pass

    def forget_last_assumption(self) -> None:
        pass

    class Factory(ABC):

        @abstractmethod
        def create(
            self,
            bot:PlayerId) -> OpponentModel:
            pass


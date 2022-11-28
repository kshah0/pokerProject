from abc import ABC, abstractmethod
from typing import Dict
from gametree.playerstate.player_id import PlayerId
from gametree.playerstate.player_state import PlayerState

from __future__ import annotations

from gametree.gamestate.game_state import GameState
from gametree.mcts.nodes.inode import INode

class OpponentModel(ABC):

    @abstractmethod
    def get_action_probs(self, gs:GameState, ps:PlayerState) -> Dict[str,float]:
        pass
    

    @abstractmethod
    def get_bot_id() -> PlayerId:
        pass

    # May not need these 2 functions below
    @abstractmethod
    def set_chosen_node(self, node:INode) -> None:
        pass

    @abstractmethod
    def get_chosen_node() -> INode:
        pass
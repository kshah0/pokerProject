from abc import ABC
from typing import Any, List, Tuple

from node import NodeType, node_type_from_game_state
from player_interface import PlayerAction

class PokerGameState:
    pass

class PokerMove(ABC):
    action: Any

class PokerMovePlayer(PokerMove):
    action: PlayerAction
    amount: Union[float, None] 

def next_moves(game_state: PokerGameState) -> List[PokerMove]:
    node_type = node_type_from_game_state(game_state)
    res = []
    if node_type == NodeType.PLAYER:
        pass
    elif node_type == NodeType.OPPONENT:
        pass
    else:
        pass
    return res

def is_over(game_state: PokerGameState) -> Tuple[bool, float]:
    pass
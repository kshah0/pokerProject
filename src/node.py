from enum import Enum
from game_state import PokerGameState, PokerMove
from typing import Dict, Union
from __future__ import annotations

class NodeType(Enum):
    PLAYER = 0
    OPPONENT = 1
    CHANCE = 2

class Node:
    game_state: PokerGameState
    parent: Union[None, Node]
    children: Dict[PokerMove, Node]
    total_value: float
    num_episodes: int
    node_type: NodeType

    def __init__(
        self,
        game_state: PokerGameState,
        parent: Union[None, Node],
        children: Dict[PokerMove, Node] = {},
        total_value: float = 0.0,
        num_episodes: int = 0,
    ):
        self.game_state = game_state
        self.parent = parent
        self.children = children
        self.total_value = total_value
        self.num_episodes = num_episodes
        # I'm assuming that the node type can be inferred from the game state, but if not we can just pass it in directly
        self.node_type = node_type_from_game_state(game_state)

    def get_expected_value(self):
        return self.total_value/self.num_episodes

def node_type_from_game_state(game_state: PokerGameState) -> NodeType:
    pass
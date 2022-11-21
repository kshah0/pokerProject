from abc import ABC
from typing import Any, List, Tuple, Union
from card import Card

from node import NodeType, node_type_from_game_state
from player_interface import PlayerAction

class PokerGameState:
    pass

class PokerMove(ABC):
    action: Any

class PokerMovePlayer(PokerMove):
    # For player OR opponent nodes
    action: PlayerAction
    amount: Union[float, None] # amount to raise for RAISE, None for all other player actions

    def __init__(self, action: PlayerAction, amount = None):
        self.action = action
        self.amount = amount

    def __eq__(self, __o: object) -> bool:
        return (
            self.action == __o.action and
            self.amount == __o.amount
        )

class PokerMoveCommunity(PokerMove):
    # For chance nodes
    action: Card # card that was dealt

    def __init__(self, card: Card):
        self.action = card

    def __eq__(self, __o: object) -> bool:
        return self.action == __o.action

def next_moves(game_state: PokerGameState) -> List[PokerMove]:
    node_type = node_type_from_game_state(game_state)
    res = []
    if node_type == NodeType.CHANCE:
        # List all possible cards that could be dealt (Anything that's not visible to the player)
        pass
    else:
        # TODO: only add actions if player hasn't already folded
        for action in PlayerAction:
            if action == PlayerAction.RAISE:
                continue
            res.append(PokerMovePlayer(action))
        # TODO: Check if player is able to raise
        # TODO: Set these variables based on game state (bet increment is a parameter)
        max_bet = 50
        bet_increment = 0.5
        min_bet = bet_increment

        raise_amount = min_bet
        while raise_amount <= max_bet:
            res.append(PokerMovePlayer(PlayerAction.RAISE, raise_amount))
            raise_amount += bet_increment
    return res

def is_over(game_state: PokerGameState) -> Tuple[bool, float]:
    pass
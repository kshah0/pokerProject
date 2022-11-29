from abc import ABC
from typing import List, Set
from card import Card
from gametree.action.probability_action import ProbabilityAction

from gametree.playerstate.abstract_player_state import AbstractPlayerState
from gametree.playerstate.player_id import PlayerId
from gametree.playerstate.player_state import PlayerState
from gametree.playerstate.seat_id import SeatId


class ForwardingPlayerState(AbstractPlayerState, ABC):
    player_state: PlayerState

    def __init__(self, player_state: PlayerState) -> None:
        self.player_state = player_state
    
    def get_bet(self) -> int:
        return self.player_state.get_bet()

    # @Override
    def get_name(self) -> str:
        return self.player_state.get_name()

    # @Override
    def get_total_investment(self) -> int:
        return self.player_state.get_total_investment()

    # @Override
    def get_cards(self) -> Set[Card]:
        return self.player_state.get_cards()

    # @Override
    def get_stack(self) -> int:
        return self.player_state.get_stack()

    # @Override
    def has_folded(self) -> bool:
        return self.player_state.has_folded()

    # @Override
    def get_seat_id(self) -> SeatId:
        return self.player_state.get_seat_id()

    # @Override
    def get_player_id(self) -> PlayerId:
        return self.player_state.get_player_id()

    # @Override
    def has_checked(self) -> bool:
        return self.player_state.has_checked()

    # @Override
    def has_checked(self) -> List[int]:
        return self.player_state.get_bet_progression()

    def get_prev_action(self) -> ProbabilityAction:
        return self.player_state.get_prev_action()
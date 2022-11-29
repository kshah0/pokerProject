from typing import Set, List
from card import Card
from gametree.action.probability_action import ProbabilityAction
from gametree.playerstate.abstract_player_state import AbstractPlayerState
from gametree.playerstate.player_id import PlayerId
from gametree.playerstate.seat_id import SeatId


class SeatedPlayerState(AbstractPlayerState):
    player: SeatedPlayer

    def __init__(self, player: SeatedPlayer) -> None:
        self.player = player

    def get_name(self) -> str:
        return self.player.get_name()

    def has_folded(self) -> bool:
        return False

    def get_stack(self) -> int:
        return self.player.get_stack_value()

    def get_seat_id(self) -> SeatId:
        return self.player.get_seat_id()

    def get_player_id(self) -> PlayerId:
        return self.player.get_id()

    def get_cards(self) -> Set[Card]:
        return super().get_cards()

    def get_bet_progression(self) -> List[int]:
        return [self.player.get_bet_chips_value()]

    def get_bet(self) -> int:
        return self.player.get_bet_chips_value()

    def get_total_investment(self) -> int:
        return self.player.get_bet_chips_value()

    def has_been_dealt(self) -> bool:
        return False

    def has_checked(self) -> bool:
        return False

    def get_prev_action(self) -> ProbabilityAction:
        return self.player.get_prev_action()
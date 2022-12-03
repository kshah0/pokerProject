from gametree.action.call_action import CallAction
from gametree.action.check_action import CheckAction
from gametree.action.fold_action import FoldAction
from gametree.action.probability_action import ProbabilityAction
from gametree.playerstate.player import Player
from gametree.playerstate.player_id import PlayerId
from gametree.playerstate.seat_id import SeatId

class SeatedPlayer(Player):
    seat_id: SeatId
    has_cards: bool
    stack_value: int
    bet_chips_value: int
    sitting_in: bool
    prev_action: ProbabilityAction

    def __init__(self,
        player_id: PlayerId,
        seat_id: SeatId,
        name: str,
        stack_value: int,
        bet_chips_value: int,
        sitting_in: bool,
        has_cards: bool,
        prev_action: ProbabilityAction = None,
    ) -> None:
        super().__init__(player_id, name)
        self.seat_id = seat_id
        self.stack_value = stack_value
        self.bet_chips_value = bet_chips_value
        self.sitting_in = sitting_in
        self.has_cards = has_cards
        self.prev_action = prev_action

    def get_seat_id(self):
        return self.seat_id

    def get_stack_value(self):
        return self.stack_value

    def get_bet_chips_value(self):
        return self.bet_chips_value

    def is_sitting_in(self):
        return self.sitting_in

    def has_cards(self):
        return self.has_cards

    def get_prev_action(self) -> int:
        """returns -1 for fold, 0 for call/check, 1+ for raise (raise amount)"""
        if isinstance(self.prev_action, FoldAction):
            return -1
        if (
            isinstance(self.prev_action, CallAction)
            or isinstance(self.prev_action, CheckAction)
        ):
            return 0
        else: # is BetAction or CheckAction
            return self.prev_action.amount
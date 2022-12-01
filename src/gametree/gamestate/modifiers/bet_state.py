
from typing import List
from gametree.gamestate.forwarding_game_state import ForwardingGameState
from gametree.gamestate.game_state import GameState
from gametree.gamestate.modifiers.events.bet_event import BetEvent
from gametree.playerstate.forwarding_player_state import ForwardingPlayerState
from gametree.playerstate.player_id import PlayerId
from gametree.playerstate.player_state import PlayerState
from __future__ import annotations

from gametree.round import Round


class BetPlayerState(ForwardingPlayerState):
    def __init__(self, player_state: PlayerState, bet_state: BetState) -> None:
        super().__init__(player_state)
        self.bet_state = bet_state

    def get_bet(self) -> int:
        if self.bet_state.bet_after_blind_case:
            return super().get_bet() + self.bet_state.event.amount
        return self.bet_state.event.amount

    def get_total_investment(self) -> int:
        return super().get_total_investment() + self.bet_state.event.amount

    def get_stack(self) -> int:
        return self.bet_state.new_stack

    def get_player_id(self) -> PlayerId:
        return self.bet_state.event.player_id

    def has_folded(self) -> bool:
        return False

    def has_been_dealt(self) -> bool:
        return True

    def has_checked(self) -> List[int]:
        return False

    def get_bet_progression(self) -> List[int]:
        if self.bet_state.bet_after_blind_case:
            result = []
            last_bettor_id = self.bet_state.game_state.get_last_bettor()
            last_bettor = self.bet_state.game_state.get_player(last_bettor_id)
            previous_bet_progression = last_bettor.get_bet_progression()
            result += previous_bet_progression
            result += [self.bet_state.event.amount]
            return result
        return [self.get_bet()]

class BetState(ForwardingGameState):
    event: BetEvent
    new_pot_size: int
    player_state: PlayerState
    bet_after_blind_case: bool
    new_stack: int
    

    def __init__(self, game_state: GameState, event: BetEvent) -> None:
        super().__init__(game_state)
        self.event = event
        old_player_state = super().get_player(event.player_id)

        self.bet_after_blind_case = Round.PREFLOP == game_state.get_round()

        if self.bet_after_blind_case and game_state.get_deficit(event.player_id) > 0:
            raise RuntimeError("Can't bet in the preflop round when you have a deficit to pay")

        self.new_stack = old_player_state.get_stack() - event.amount

        self.new_pot_size = super().get_round_pot_size() + event.amount
        self.player_state = BetPlayerState(old_player_state, self)

    def get_player(self, player_id: PlayerId) -> PlayerState:
        if self.event.player_id == player_id:
            return self.player_state
        return super().get_player(player_id)

    def get_largest_bet(self) -> int:
        if self.bet_after_blind_case:
            return super().get_largest_bet() + self.event.amount
        return self.event.amount
    
    def get_min_next_raise(self) -> int:
        return self.event.amount

    def get_round_pot_size(self) -> int:
        return self.new_pot_size

    def get_last_event(self):
        return self.event

    def get_last_bettor(self) -> PlayerId:
        return self.event.player_id

    def get_num_raises(self) -> int:
        return 1

    def get_event(self):
        return self.event
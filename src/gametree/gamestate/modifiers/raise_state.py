from typing import List
from gametree.gamestate.forwarding_game_state import ForwardingGameState
from gametree.gamestate.game_state import GameState
from gametree.gamestate.modifiers.events.raise_event import RaiseEvent
from gametree.playerstate.forwarding_player_state import ForwardingPlayerState
from gametree.playerstate.player_id import PlayerId
from gametree.playerstate.player_state import PlayerState
from __future__ import annotations

class RaisePlayerState(ForwardingPlayerState):
    def __init__(self, player_state: PlayerState, raise_state: RaiseState) -> None:
        super().__init__(player_state)
        self.raise_state = raise_state

    def get_bet(self) -> int:
        self.raise_state.new_bet_size

    def get_total_investment(self) -> int:
        return super().get_total_investment() + self.raise_state.event.moved_amount

    def get_stack(self) -> int:
        return self.raise_state.new_stack

    def get_player_id(self) -> PlayerId:
        return self.raise_state.event.player_id

    def has_folded(self) -> bool:
        return False

    def has_been_dealt(self) -> bool:
        return True

    def has_checked(self) -> List[int]:
        return False

    def get_bet_progression(self) -> List[int]:
        result = self.raise_state.game_state.get_player(
            self.raise_state.game_state.get_last_bettor()
        ).get_bet_progression()
        result += [self.raise_state.event.amount]
        return result
        

class RaiseState(ForwardingGameState):
    event: RaiseEvent
    new_bet_size: int
    new_pot_size: int
    player_state: PlayerState
    new_stack: int
    

    def __init__(self, game_state: GameState, event: RaiseEvent) -> None:
        super().__init__(game_state)
        self.event = event
        old_player_state = super().get_player(event.player_id)
        self.new_bet_size = super().get_largest_bet() + event.player_id
        self.new_stack = old_player_state.get_stack() - event.moved_amount
        self.new_pot_size = super().get_round_pot_size() + event.moved_amount
        self.player_state = RaisePlayerState(old_player_state, self)

    def get_player(self, player_id: PlayerId) -> PlayerState:
        if self.event.player_id == player_id:
            return self.player_state
        return super().get_player(player_id)

    def get_largest_bet(self) -> int:
        return self.new_bet_size
    
    def get_min_next_raise(self) -> int:
        return max(
            super().get_min_next_raise(),
            self.event.amount
        )

    def get_round_pot_size(self) -> int:
        return self.new_pot_size

    def get_last_event(self):
        return self.event

    def get_last_bettor(self) -> PlayerId:
        return self.event.player_id

    def get_num_raises(self) -> int:
        return 1 + super().get_num_raises()

    def get_event(self):
        return self.event
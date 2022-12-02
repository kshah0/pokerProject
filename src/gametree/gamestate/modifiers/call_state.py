from typing import List
from gametree.gamestate.forwarding_game_state import ForwardingGameState
from gametree.gamestate.game_state import GameState
from gametree.gamestate.modifiers.events.call_event import CallEvent
from gametree.playerstate.forwarding_player_state import ForwardingPlayerState
from gametree.playerstate.player_id import PlayerId
from gametree.playerstate.player_state import PlayerState
from __future__ import annotations

class CallPlayerState(ForwardingPlayerState):
    def __init__(self, player_state: PlayerState, call_state: CallState) -> None:
        super().__init__(player_state)
        self.call_state = call_state

    def get_bet(self) -> int:
        return self.call_state.new_bet_size

    def get_total_investment(self) -> int:
        return super().get_total_investment() + self.call_state.chips_moved

    def get_stack(self) -> int:
        return self.call_state.new_stack

    def get_player_id(self) -> PlayerId:
        return self.call_state.event.player_id

    def has_folded(self) -> bool:
        return False

    def has_been_dealt(self) -> bool:
        return True

    def has_checked(self) -> List[int]:
        return False

    def get_bet_progression(self) -> List[int]:
        return self.call_state.game_state.get_player(
            self.call_state.game_state.get_last_bettor()
        ).get_bet_progression()

class CallState(ForwardingGameState):
    event: CallEvent
    new_pot_size: int
    player_state: PlayerState
    new_stack: int
    chips_moved: int
    new_bet_size: int

    def __init__(self, game_state: GameState, event: CallEvent) -> None:
        super().__init__(game_state)
        self.event = event
        self.new_bet_size = super().get_largest_bet()
        player = super().get_player(event.player_id)
        self.chips_moved = self.new_bet_size - player.get_bet()
        self.new_stack = player.get_stack() - self.chips_moved

        self.new_pot_size = super().get_round_pot_size() + self.chips_moved
        self.player_state = CallPlayerState(player, self)

    def get_player(self, player_id: PlayerId) -> PlayerState:
        if self.event.player_id == player_id:
            return self.player_state
        return super().get_player(player_id)

    def get_round_pot_size(self) -> int:
        return self.new_pot_size

    def get_last_event(self):
        return self.event

    def get_event(self):
        return self.event
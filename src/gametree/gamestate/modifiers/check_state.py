from typing import List
from gametree.gamestate.forwarding_game_state import ForwardingGameState
from gametree.gamestate.game_state import GameState
from gametree.gamestate.modifiers.events.check_event import CheckEvent
from gametree.playerstate.forwarding_player_state import ForwardingPlayerState
from gametree.playerstate.player_id import PlayerId
from gametree.playerstate.player_state import PlayerState
from __future__ import annotations

from gametree.round import Round


class CheckPlayerState(ForwardingPlayerState):
    def __init__(self, player_state: PlayerState, check_state: CheckState) -> None:
        super().__init__(player_state)
        self.check_state = check_state

    def get_bet(self) -> int:
        if self.check_state.check_after_blind_case:
            return super().get_bet()
        return 0

    def get_player_id(self) -> PlayerId:
        return self.check_state.event.player_id

    def has_folded(self) -> bool:
        return False

    def has_been_dealt(self) -> bool:
        return True

    def has_checked(self) -> List[int]:
        return True

class CheckState(ForwardingGameState):
    event: CheckEvent
    player_state: PlayerState
    check_after_blind_case: bool
    new_pot_size: int

    def __init__(self, game_state: GameState, event: CheckEvent) -> None:
        super().__init__(game_state)
        self.event = event
        player = game_state.get_player(event.player_id)
        
        self.check_after_blind_case = Round.PREFLOP == game_state.get_round()

        if (
            self.check_after_blind_case
            and game_state.get_deficit(event.player_id) > 0
        ):
            raise RuntimeError("Can't check in the preflop round when you have a deficit to pay.")

        self.new_pot_size = super().get_round_pot_size()
        self.player_state = CheckPlayerState(player, self)

    def get_player(self, player_id: PlayerId) -> PlayerState:
        if self.event.player_id == player_id:
            return self.player_state
        return super().get_player(player_id)

    def get_round_pot_size(self) -> int:
        return self.new_pot_size

    def get_last_event(self):
        return self.event

    def get_largest_bet(self) -> int:
        if self.check_after_blind_case:
            return super().get_largest_bet()
        return 0

    def get_last_bettor(self) -> PlayerId:
        if self.check_after_blind_case:
            return super().get_last_bettor()
        return None

    def get_num_raises(self) -> int:
        return 0

    def get_event(self):
        return self.event
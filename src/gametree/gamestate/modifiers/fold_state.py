from typing import List
from gametree.gamestate.forwarding_game_state import ForwardingGameState
from gametree.gamestate.game_state import GameState
from gametree.gamestate.modifiers.events.fold_event import FoldEvent
from gametree.playerstate.forwarding_player_state import ForwardingPlayerState
from gametree.playerstate.player_id import PlayerId
from gametree.playerstate.player_state import PlayerState
from __future__ import annotations


class FoldPlayerState(ForwardingPlayerState):
    def __init__(self, player_state: PlayerState, fold_state: FoldState) -> None:
        super().__init__(player_state)
        self.fold_state = fold_state

    def get_bet(self) -> int:
        self.player_state.get_bet_progression()

    def get_player_id(self) -> PlayerId:
        return self.fold_state.event.player_id

    def has_folded(self) -> bool:
        return True

    def has_been_dealt(self) -> bool:
        return True

    def has_checked(self) -> List[int]:
        return False

class FoldState(ForwardingGameState):
    event: FoldEvent
    player_state: PlayerState

    def __init__(self, game_state: GameState, event: FoldEvent) -> None:
        super().__init__(game_state)
        self.event = event
        old_player_state = super().get_player(event.player_id)
        self.player_state = FoldPlayerState(old_player_state, self)

    def get_player(self, player_id: PlayerId) -> PlayerState:
        if self.event.player_id == player_id:
            return self.player_state
        return super().get_player(player_id)

    def get_last_event(self):
        return self.event

    def get_event(self):
        return self.event
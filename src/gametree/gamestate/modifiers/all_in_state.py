from typing import List
from gametree.gamestate.forwarding_game_state import ForwardingGameState
from gametree.gamestate.game_state import GameState
from gametree.playerstate.forwarding_player_state import ForwardingPlayerState
from gametree.playerstate.player_id import PlayerId
from gametree.playerstate.player_state import PlayerState
from __future__ import annotations

class AllInPlayerState(ForwardingPlayerState):
    def __init__(self, player_state: PlayerState, all_in_state: AllInState) -> None:
        super().__init__(player_state)
        self.all_in_state = all_in_state

    def get_bet(self) -> int:
        self.all_in_state.new_bet_size

    def get_total_investment(self) -> int:
        return super().get_total_investment() + self.all_in_state.event.get_moved_amount()

    def get_stack(self) -> int:
        return 0

    def get_player_id(self) -> PlayerId:
        return self.all_in_state.event.get_player_id()

    def has_folded(self) -> bool:
        return False

    def has_checked(self) -> List[int]:
        return False

    def has_been_dealt(self) -> bool:
        return True

    def get_bet_progression(self) -> List[int]:
        result = []
        if self.all_in_state.game_state.get_last_bettor() is not None:
            result += self.all_in_state.game_state.get_player(
                self.all_in_state.game_state.get_last_bettor()
            ).get_bet_progression()
        result += self.all_in_state.event.get_moved_amount()
        return result

class AllInState(ForwardingGameState):
    event: AllInEvent
    new_pot_size: int
    raise_amount: int
    player_state: PlayerState
    new_bet_size: int
    

    def __init__(self, game_state: GameState, event: AllInEvent) -> None:
        super().__init__(game_state)
        self.event = event
        player = super().get_player(event.get_player_id())
        self.new_pot_size = super().get_round_pot_size() + event.get_moved_amount()
        self.new_bet_size = player.get_bet() + event.get_moved_amount()
        self.raise_amount = max(
            self.new_bet_size - super().get_largest_bet(),
            0
        )
        self.player_state = AllInPlayerState(player, self)

    def get_player(self, player_id: PlayerId) -> PlayerState:
        if self.event.get_player_id() == player_id:
            return self.player_state
        return super().get_player(player_id)

    def get_largest_bet(self) -> int:
        if self.raise_amount > 0:
            return self.new_bet_size
        return super().get_largest_bet()
    
    def get_min_next_raise(self) -> int:
        return max(self.raised_amount, super().get_min_next_raise())

    def get_round_pot_size(self) -> int:
        return self.new_pot_size

    def get_last_event(self):
        return self.event

    def get_last_bettor(self) -> PlayerId:
        if self.raise_amount > 0:
            return self.event.get_player_id()
        return super().get_last_bettor()

    def get_num_raises(self) -> int:
        prev_num_raises = super().get_num_raises()
        if self.raise_amount > 0:
            return prev_num_raises + 1
        return prev_num_raises

    def get_raise(self):
        return self.raise_amount

    def get_event(self):
        return self.event
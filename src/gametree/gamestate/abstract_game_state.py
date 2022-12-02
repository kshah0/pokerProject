from abc import ABC
import copy
from typing import Set
from gametree.gamestate.game_state import GameState
from gametree.playerstate.player_id import PlayerId
from gametree.playerstate.player_state import PlayerState
from gametree.playerstate.seat_id import SeatId


class AbstractGameState(GameState, ABC):

    def get_deficit(self, player_id: PlayerId) -> int:
        return self.get_largest_bet() - self.get_player(player_id).get_bet()

    def get_call_value(self, player_id: PlayerId) -> int:
        player = self.get_player(player_id)
        return min(self.get_largest_bet() - player.get_bet(), player.get_stack())

    def is_allowed_to_raise(self, player_id: PlayerId) -> bool:
        player = self.get_player(player_id)
        if (
            self.get_largest_bet() - player.get_bet() >= player.get_stack()
        ):
            return False
        other_players = self.get_all_seated_players()
        for other_player in other_players:
            # check whether we are the only active player left in the game
            if (
                not other_player.get_player_id() == player_id
                and other_player.is_actively_playing()
            ):
                return True
        return False

    def get_lower_raise_bound(self, player_id: PlayerId) -> int:
        player = self.get_player(player_id)
        return max(
            0,
            min(
                self.get_min_next_raise(),
                player.get_stack() - (self.get_largest_bet() - player.get_bet())
            )
        )
    
    def get_upper_raise_bound(self, player_id: PlayerId) -> int:
        player = self.get_player(player_id)
        temp_id = player_id
        max_other_bettable_chips = 0
        while True:
            # TODO: (from cspoker) fix infinite loop on double BB
            temp_player = self.get_next_active_player_after(temp_id)
            if temp_player is None:
                break
            temp_id = temp_player.get_player_id()
            if temp_player.get_player_id() != player_id:
                max_other_bettable_chips = max(
                    max_other_bettable_chips,
                    temp_player.get_bet() + temp_player.get_stack()
                )
            else:
                break
        bettable_chips = min(
            player.get_stack() + player.get_bet(),
            max_other_bettable_chips
        )

        return max(0, bettable_chips - self.get_largest_bet())

    def get_game_pot_size(self) -> int:
        return self.get_previous_rounds_pot_size() + self.get_round_pot_size()

    def has_bet(self) -> bool:
        return self.get_largest_bet() > 0

    def get_all_seated_players(self) -> Set[PlayerState]:
        ids = set(self.seat_map.values())
        states = set()
        for player_id in ids:
            states.add(self.get_player(player_id))
        return states

    def get_default_winner(self) -> PlayerState:
        ids = self.seat_map.values()
        first = None
        for player_id in ids:
            state = self.get_player(player_id)
            if not state.has_folded():
                if first is not None:
                    return None
                first = state
        return first

    def get_next_seated_player_after(self, start_player: PlayerId) -> PlayerState:
        max_num_players = self.table_config.get_max_num_players()
        current_seat = list(self.seat_map.keys())[list(self.seat_map.values()).index(start_player)]
        while True:
            current_seat = SeatId((current_seat.get_id() + 1) % max_num_players)
            current_player = self.seat_map.get(current_seat)
            if current_player is not None:
                break
        if current_player == start_player:
            return None
        return self.get_player(current_player)

    def get_next_active_player_after(self, start_player_id: PlayerId) -> PlayerState:
        current_player_id = start_player_id
        while True:
            current_player = self.get_next_seated_player_after(current_player_id)
            if current_player is None:
                return None
            current_player_id = current_player.get_player_id()
            if current_player_id == start_player_id:
                return None
            if current_player.is_actively_playing():
                break
        return current_player

    # def accept_history_visitor(self, visitor: GameStateVisitor, start: GameState) -> None:
    #     if self != start:
    #         self.get_previous_game_state().accept_history_visitor(visitor, start)
    #         self.accept_visitor(visitor)
    
    def __str__(self) -> str:
        return self.get_last_event() + '\n' + self.get_previous_game_state()
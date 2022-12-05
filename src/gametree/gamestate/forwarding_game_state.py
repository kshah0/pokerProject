from abc import ABC
from typing import Set
from card import Card

from gametree.gamestate.abstract_game_state import AbstractGameState
from gametree.gamestate.game_state import GameState
from gametree.playerstate.player_id import PlayerId
from gametree.playerstate.player_state import PlayerState
from gametree.round import Round


class ForwardingGameState(AbstractGameState, ABC):
    game_state: GameState

    def __init__(self, game_state: GameState) -> None:
        self.game_state = game_state

    def get_largest_bet(self) -> int:
        return self.game_state.get_largest_bet()

    def get_min_next_raise(self) -> int:
        return self.game_state.get_min_next_raise()

    def get_previous_rounds_pot_size(self) -> int:
        return self.game_state.get_previous_rounds_pot_size()

    def get_round_pot_size(self) -> int:
        return self.game_state.get_round_pot_size()

    def get_round(self) -> Round:
        return self.game_state.get_round()

    def get_community_cards(self) -> Set[Card]:
        return self.game_state.get_community_cards()

    def get_dealer(self) -> PlayerId:
        return self.game_state.get_dealer()

    def get_previous_game_state(self) -> GameState:
        return self.game_state

    def get_last_bettor(self) -> PlayerId:
        return self.game_state.get_last_bettor()

    def get_next_to_act(self) -> PlayerId:
        return self.game_state.get_next_to_act()

    def get_player(self, player_id: PlayerId) -> PlayerState:
        return self.game_state.get_player(player_id)
    
    def get_big_blind(self) -> PlayerId:
        return self.game_state.get_big_blind()

    def get_small_blind(self) -> PlayerId:
        return self.game_state.get_small_blind()

    def get_num_raises(self) -> int:
        return self.game_state.get_num_raises()
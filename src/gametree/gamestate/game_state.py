from abc import ABC, abstractmethod
from typing import Dict, Set
from card import Card

from gametree.playerstate.player_id import PlayerId
from __future__ import annotations

from gametree.playerstate.player_state import PlayerState


class GameState(ABC):
    
    table_config: TableConfiguration
    seat_map: Dict[SeatId, PlayerId]

    @abstractmethod
    def get_player(self, player_id: PlayerId) -> PlayerState:
        pass

    @abstractmethod
    def get_all_seated_players(self) -> Set[PlayerState]:
        pass

    @abstractmethod
    def get_dealer(self) -> PlayerId:
        pass

    @abstractmethod
    def get_last_bettor(self) -> PlayerId:
        pass

    @abstractmethod
    def get_next_to_act(self) -> PlayerId:
        pass

    @abstractmethod
    def get_previous_rounds_pot_size(self) -> int:
        pass

    @abstractmethod
    def get_round_pot_size(self) -> int:
        pass

    @abstractmethod
    def get_game_pot_size(self) -> int:
        pass

    @abstractmethod
    def get_largest_bet(self) -> int:
        pass

    @abstractmethod
    def get_min_next_raise(self) -> int:
        pass

    @abstractmethod
    def get_round(self) -> Round:
        pass

    @abstractmethod
    def get_community_cards(self) -> Set[Card]:
        pass

    @abstractmethod
    def get_previous_game_state(self) -> GameState:
        pass

    @abstractmethod
    def get_last_event(self) -> HoldemTableTreeEvent:
        pass

    # A derived state property that is the difference between the 
    # largest bet and the current bet of a given player
    @abstractmethod
    def get_deficit(self, player_id: PlayerId) -> int:
        pass
    
    # A derived state property that is the minimum
    # of the player deficit and stack
    @abstractmethod
    def get_call_value(self, player_id: PlayerId) -> int:
        pass

    # A derived state property that is the minimum
    # of the minimal raise and stack
    @abstractmethod
    def get_lower_raise_bound(self, player_id: PlayerId) -> int:
        pass

    @abstractmethod
    def get_upper_raise_bound(self, player_id: PlayerId) -> int:
        pass

    # A derived state property whether the player has enough money to raise
    @abstractmethod
    def is_allowed_to_raise(self, player_id: PlayerId) -> bool:
        pass

    @abstractmethod
    def has_bet(self) -> bool:
        pass

    @abstractmethod
    def get_num_raises(self) -> int:
        pass

    @abstractmethod
    def get_next_active_player_after(self, player_id: PlayerId) -> PlayerState:
        pass

    @abstractmethod
    def get_next_seated_player_after(self, player_id: PlayerId) -> PlayerState:
        pass

    @abstractmethod
    def accept_history_visitor(self, visitor: GameStateVisitor, start: GameState) -> None:
        pass

    @abstractmethod
    def accept_visitor(self, visitor: GameStateVisitor) -> None:
        pass

    # Get the PlayerState of the only player left for the pot, None if there are multiple left
    @abstractmethod
    def get_default_winner(self) -> PlayerState:
        pass

    @abstractmethod
    def get_big_blind(self) -> PlayerId:
        pass

    @abstractmethod
    def get_small_blind(self) -> PlayerId:
        pass
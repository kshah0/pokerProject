from abc import ABC, abstractmethod
from typing import List, Set
from card import Card
from gametree.action.probability_action import ProbabilityAction

from gametree.playerstate.player_id import PlayerId
from gametree.playerstate.seat_id import SeatId


class PlayerState(ABC):
    @abstractmethod
    def get_player_id(self) -> PlayerId:
        pass

    @abstractmethod
    def get_seat_id(self) -> SeatId:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_cards(self) -> Set[Card]:
        pass

    @abstractmethod
    def get_stack(self) -> int:
        pass

    @abstractmethod
    def get_bet(self) -> int:
        pass

    @abstractmethod
    def get_total_investment(self) -> int:
        pass

    @abstractmethod
    def get_bet_progression(self) -> List[int]:
        pass

    @abstractmethod
    def has_folded(self) -> bool:
        pass

    @abstractmethod
    def has_been_dealt(self) -> bool:
        pass
    
    @abstractmethod
    def is_all_in(self) -> bool:
        pass

    @abstractmethod
    def is_actively_playing(self) -> bool:
        pass

    @abstractmethod
    def has_checked(self) -> bool:
        pass

    @abstractmethod
    def get_prev_action(self) -> ProbabilityAction:
        pass
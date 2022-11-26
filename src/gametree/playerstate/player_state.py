from abc import ABC, abstractmethod
from typing import List, Set
from card import Card

from gametree.playerstate.player_id import PlayerId


class PlayerState(ABC):
    player_id: PlayerId
    seat_id: SeatId
    name: str
    cards: Set[Card]

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
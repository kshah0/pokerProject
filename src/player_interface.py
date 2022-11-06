from abc import ABC, abstractmethod
from game_deck import GameDeck
from player_hand import PlayerHand
from typing import List, Tuple
import enum

class PlayerAction(enum.Enum):
    # Design Decision: Players will "CHECK" when all-in for logic in the game to work out
    CHECK           = 0
    CALL            = 1
    RAISE           = 2
    FOLD            = 3
    END_OF_STREET   = 4

class Player(ABC):
    def __init__(self, stack_size) -> None:
        self.stack_size: float = stack_size
        self.current_bet: float = 0
        self.hand: PlayerHand = None
        self.active: bool = True
        self.history: List[Tuple(PlayerAction, float)] = []

    def set_hand(self, hand: PlayerHand) -> None:
        self.hand = hand

    @abstractmethod
    # Expected to update stack_size, current_bet, active, and history internally
    def action(self, position: int, players: List, deck: GameDeck, pot_size: float) -> Tuple(PlayerAction, float):
        pass

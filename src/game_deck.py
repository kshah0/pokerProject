from card import Card
from player_hand import PlayerHand
from typing import List
import random

# Simulates a deck and board runout in a single run of the game
class GameDeck:
    # Shuffles deck and "deals" cards to players
    def __init__(self, num_players: int) -> None:
        self.num_players = num_players
        self.deck: List[Card] = [Card(a+b) for a in Card.card_order_dict.keys() for b in Card.suits]
        random.shuffle(self.deck)
        self.board_cards_dealt = 0
    
    # Get the hand of the i-th player (0-indexed)
    def get_player_hand(self, i) -> PlayerHand:
        return PlayerHand(self.deck[ 2*i : 2*i + 2 ])

    # Returns list of cards on the board for all players to use
    def get_board(self) -> List[Card]:
        return self.deck[2 * self.num_players : 2 * self.num_players + self.board_cards_dealt]

    # Determines if it is showdown time
    def is_showdown(self) -> bool:
        return self.board_cards_dealt == 5

    # Simulates dealing cards to the board
    def deal_board_card(self) -> None: 
        if self.board_cards_dealt == 0:
            self.board_cards_dealt = 2
        self.board_cards_dealt += 1

    def __str__(self) -> str:
        prefix = ["Pre-Flop", '', '', "Flop", "Turn", "River"][self.board_cards_dealt]
        return f"{prefix}: {' '.join([str(card) for card in self.get_board()])}"

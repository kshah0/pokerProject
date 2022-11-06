from card import Card
from hand_ranking import HandRanking, evaluate_hand
from typing import List, Tuple
import itertools

# Represents a player hand in a single run of the game
class PlayerHand:
    def __init__(self, cards: List[Card]) -> None:
        if cards[0] < cards[1]:
            cards[0], cards[1] = cards[1], cards[0]
        self.cards: List[Card] = cards
    
    # Create best Texas hold 'em hand with community cards
    def get_best_hand(self, cards: List[Card]) -> Tuple[HandRanking, List[int], List[Card]]:
        # If we are looking at a preflop scenario, just check for pocket pair
        if len(cards) < 3:
            value = HandRanking.HIGH_CARD
            if self.cards[0].rank == self.cards[1].rank:
                value = HandRanking.ONE_PAIR
            return (value, [Card.card_order_dict[c.rank] for c in self.cards], self.cards)
        # Otherwise evaluate all combinations with community cards
        best = (HandRanking.HIGH_CARD, [], [])
        for used in [list(i) for i in itertools.combinations(cards, 3)]:
            hand = sorted(used + self.cards, reverse=True)
            best = max(best, (*evaluate_hand(hand), hand))
        return best

    def __str__(self) -> str:
        return f'{str(self.cards[0])} {str(self.cards[1])}'

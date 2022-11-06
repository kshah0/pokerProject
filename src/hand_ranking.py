from card import Card
from typing import List, Tuple
import enum
from functools import total_ordering
from collections import defaultdict

@total_ordering
class HandRanking(enum.Enum):
    STRAIGHT_FLUSH      = 8
    FOUR_OF_A_KIND      = 7
    FULL_HOUSE          = 6
    FLUSH               = 5
    STRAIGHT            = 4
    THREE_OF_A_KIND     = 3
    TWO_PAIR            = 2
    ONE_PAIR            = 1
    HIGH_CARD           = 0

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

# All functions assume that hands are sorted by decreasing rank prior to use

def evaluate_hand(hand: List[Card]) -> Tuple[HandRanking, List[int]]:
    func_and_result = \
                    [
                        (check_straight_flush, HandRanking.STRAIGHT_FLUSH),
                        (check_four_of_a_kind, HandRanking.FOUR_OF_A_KIND),
                        (check_full_house, HandRanking.FULL_HOUSE),
                        (check_flush, HandRanking.FLUSH),
                        (check_straight, HandRanking.STRAIGHT),
                        (check_three_of_a_kind, HandRanking.THREE_OF_A_KIND),
                        (check_two_pair, HandRanking.TWO_PAIR),
                        (check_one_pair, HandRanking.ONE_PAIR),
                        (check_high_card, HandRanking.HIGH_CARD),
                    ]

    for fr in func_and_result:
        ret = fr[0](hand)
        if ret[0]:
            return (fr[1], ret[1])
    raise RuntimeError(f"Failed to evaluate hand: {' '.join([str(card) for card in hand])}")

def check_straight_flush(hand: List[Card]) -> Tuple[bool, List[int]]:
    flush = check_flush(hand)
    if not flush[0]:
        return (False, 0)
    straight = check_straight(hand)
    if straight[0]:
        return straight
    return (False, 0)

def check_four_of_a_kind(hand: List[Card]) -> Tuple[bool, List[int]]:
    rank_values = [Card.card_order_dict[card.rank] for card in hand]
    if rank_values[0] == rank_values[3]:
        return (True, [rank_values[0], rank_values[4]])
    elif rank_values[1] == rank_values[4]:
        return (True, [rank_values[1], rank_values[0]])
    return (False, [])

def check_full_house(hand: List[Card]) -> Tuple[bool, List[int]]:
    rank_values = [Card.card_order_dict[card.rank] for card in hand]
    if rank_values[0] == rank_values[2] and rank_values[3] == rank_values[4]:
        return (True, [rank_values[0], rank_values[3]])
    elif rank_values[2] == rank_values[4] and rank_values[0] == rank_values[1]:
        return (True, [rank_values[2], rank_values[0]])
    return (False, [])

def check_flush(hand: List[Card]) -> Tuple[bool, List[int]]:
    return (len(set([card.suit for card in hand])) == 1, Card.card_order_dict[hand[0].rank])

def check_straight(hand: List[Card]) -> Tuple[bool, List[int]]:
    rank_values = [Card.card_order_dict[card.rank] for card in hand]
    rank_range = rank_values[0] - rank_values[-1]
    # Check for general case straight
    if len(set(rank_values)) == 5 and rank_range == 4:
        return (True, rank_values[0])
    # Check for the 5-high straight
    elif rank_values == [14, 5, 4, 3, 2]:
        return (True, 5)
    return (False, 0)

def check_three_of_a_kind(hand: List[Card]) -> Tuple[bool, List[int]]:
    rank_values = [Card.card_order_dict[card.rank] for card in hand]
    if rank_values[0] == rank_values[2]:
        return (True, [rank_values[0], rank_values[3], rank_values[4]])
    elif rank_values[1] == rank_values[3]:
        return (True, [rank_values[1], rank_values[0], rank_values[4]])
    elif rank_values[2] == rank_values[4]:
        return (True, [rank_values[2], rank_values[0], rank_values[1]])
    return (False, [])

def check_two_pair(hand: List[Card]) -> Tuple[bool, List[int]]:
    rank_values = [Card.card_order_dict[card.rank] for card in hand]
    rank_counts = defaultdict(lambda: 0)
    for v in rank_values:
        rank_counts[v] += 1
    if sorted(rank_counts.values()) == [1, 2, 2]:
        return (True, [x[1] for x in sorted([(rank_counts[v], v) for v in rank_counts.keys()], reverse=True)])
    return (False, [])

def check_one_pair(hand: List[Card]) -> Tuple[bool, List[int]]:
    rank_values = [Card.card_order_dict[card.rank] for card in hand]
    rank_counts = defaultdict(lambda: 0)
    for v in rank_values:
        rank_counts[v] += 1
    if 2 in rank_counts.values():
        return (True, [x[1] for x in sorted([(rank_counts[v], v) for v in rank_counts.keys()], reverse=True)])
    return (False, [])

def check_high_card(hand: List[Card]) -> Tuple[bool, List[int]]:
    return (True, [Card.card_order_dict[card.rank] for card in hand])

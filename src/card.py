# Represents a single card from a PlayerHand or GameDeck
class Card:
    card_order_dict: dict = {
                            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
                            "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14
                            }
    suits: set = set(['H', 'D', 'C', 'S'])

    def __init__(self, rank: str, suit: str) -> None:
        self.rank = rank
        self.suit = suit

    def __init__(self, ranksuit: str) -> None:
        self.rank = ranksuit[0]
        self.suit = ranksuit[1]

    def __lt__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.card_order_dict[self.rank] < self.card_order_dict[other.rank]
        return NotImplemented
    
    def __gt__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.card_order_dict[self.rank] > self.card_order_dict[other.rank]
        return NotImplemented

    def __str__(self) -> str:
        return self.rank + self.suit

class TableConfiguration:
    small_blind: int
    big_blind: int
    # The value of a small bet, used in the first three rounds
    small_bet: int
    # The value of a big bet, used in the fourth and final round
    big_bet: int
    # Whether dealing is done automatically
    auto_deal: bool
    # Whether blind payment is done automatically
    auto_blinds: bool
    # Whether players get the same cards in different rounds
    stratified_cards: bool
    max_num_players: int
    # The delay between two deals
    delay: int
    rake: float

    def __init__(
        self,
        small_bet: int,
        delay: int = 0,
        rake: float = 0.0,
        auto_deal: bool = True,
        stratified_cards = False,
    ) -> None:
        if not self.can_have_as_small_bet(small_bet):
            raise ValueError("Small bet invalid")
        self.small_bet = small_bet
        self.small_blind = small_bet/2
        self.big_blind = small_bet
        self.big_bet = small_bet * 2
        self.delay = delay
        self.max_num_players = 8
        self.auto_deal = auto_deal
        self.auto_blinds = True
        self.stratified_cards = stratified_cards
        self.rake = rake

    def get_small_bet(self) -> int:
        return self.small_bet

    def get_big_bet(self) -> int:
        return self.big_bet

    def can_have_as_small_bet(self, small_bet: int) -> bool:
        return (
            small_bet > 0 
            and small_bet % 2 == 0
        )

    def get_small_blind(self) -> int:
        return self.small_blind

    def get_big_blind(self) -> int:
        return self.big_blind

    def has_valid_parameters(self) -> bool:
        return (
            self.can_have_as_small_bet(self.small_bet)
            and self.get_small_blind() == self.get_small_bet()/2
            and self.get_big_blind() == self.get_small_bet()
            and self.get_big_bet() == self.get_small_bet()*2
        )

    def get_max_num_players(self) -> bool:
        return self.max_num_players

    def can_have_as_max_num_players(self, num_players: int) -> bool:
        return num_players >= 2

    def get_delay(self) -> int:
        return self.delay

    def is_closed_game(self) -> bool:
        return False

    def is_auto_blinds(self) -> bool:
        return self.auto_blinds

    def is_auto_deal(self) -> bool:
        return self.auto_deal

    def is_stratified_cards(self) -> bool:
        return self.stratified_cards

    def get_rake(self) -> float:
        return self.rake
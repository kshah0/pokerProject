from gametree.playerstate.player_id import PlayerId


class BetEvent:
    player_id: PlayerId
    amount: int

    def __init__(
        self, 
        player_id: PlayerId = None,
        amount: int = 0
    ) -> None:
        self.player_id = player_id
        self.amount = amount

    def __str__(self) -> str:
        return f"{self.player_id} bets {self.amount}."
    


from gametree.playerstate.player_id import PlayerId


class RaiseEvent:
    player_id: PlayerId
    amount: int
    moved_amount: int

    def __init__(
        self, 
        player_id: PlayerId = None,
        amount: int = 0,
        moved_amount: int = 0,
    ) -> None:
        self.player_id = player_id
        self.amount = amount
        self.moved_amount = moved_amount

    def __str__(self) -> str:
        return f"{self.player_id} raises with {self.amount}."

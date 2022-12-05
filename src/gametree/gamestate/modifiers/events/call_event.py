from gametree.playerstate.player_id import PlayerId


class CallEvent:
    player_id: PlayerId
    moved_amount: int

    def __init__(
        self, 
        player_id: PlayerId = None,
        moved_amount: int = 0
    ) -> None:
        self.player_id = player_id
        self.moved_amount = moved_amount

    def __str__(self) -> str:
        return f"{self.player_id} calls with {self.moved_amount}."
    


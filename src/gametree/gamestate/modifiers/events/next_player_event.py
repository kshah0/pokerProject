from gametree.playerstate.player_id import PlayerId

class NextPlayerEvent:
    player_id: PlayerId

    def __init__(
        self, 
        player_id: PlayerId = None,
    ) -> None:
        self.player_id = player_id

    def __str__(self) -> str:
        return f"It's {self.player_id}'s turn."
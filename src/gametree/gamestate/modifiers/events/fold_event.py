from gametree.playerstate.player_id import PlayerId

class FoldEvent:
    player_id: PlayerId

    def __init__(
        self, 
        player_id: PlayerId = None,
    ) -> None:
        self.player_id = player_id

    def __str__(self) -> str:
        return f"{self.player_id} folds."
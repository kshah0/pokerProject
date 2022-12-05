from gametree.playerstate.player_id import PlayerId


class Player:
    player_id: PlayerId
    name: str

    def __init__(self, player_id: PlayerId, name: str) -> None:
        self.player_id = player_id
        self.name = name

    def get_id(self):
        return self.player_id

    def get_name(self):
        return self.name

    def __str__(self) -> str:
        return f"{self.name} ({self.player_id})"

    def __eq__(self, __o: object) -> bool:
        if self == __o:
            return True
        if __o is None:
            return False
        if not isinstance(__o, Player):
            return False
        if self.player_id is None:
            if __o.player_id is not None:
                return False
        elif self.player_id != __o.player_id:
            return False
        return True
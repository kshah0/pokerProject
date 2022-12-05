class PlayerId:
    player_id: int

    def __init__(self, player_id):
        self.player_id = player_id

    def get_id(self):
        return self.player_id

    def __eq__(self, __o: object) -> bool:
        return self.player_id == __o.player_id

    def __str__(self) -> str:
        return f"#{self.seat_id}"
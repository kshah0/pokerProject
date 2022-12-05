class SeatId:
    seat_id: int

    def __init__(self, seat_id):
        self.seat_id = seat_id

    def get_id(self):
        return self.seat_id

    def __eq__(self, __o: object) -> bool:
        return self.seat_id == __o.seat_id

    def __str__(self) -> str:
        return f"#{self.seat_id}"
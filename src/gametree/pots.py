class Pots:
    total_value: int

    def __init__(self, total_value: int = 0) -> None:
        self.total_value = total_value

    def __str__(self) -> str:
        return f"total value in pot: {self.total_value}"
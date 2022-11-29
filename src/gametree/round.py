from enum import Enum

class Round(Enum):
    WAITING = 0
    PREFLOP = 1
    FLOP    = 2
    TURN    = 3
    FINAL   = 4

    def get_next_round(self):
        if self.value == 4:
            return None
        return Round(self.value + 1)
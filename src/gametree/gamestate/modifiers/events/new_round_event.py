from gametree.pots import Pots
from gametree.round import Round


class NewRoundEvent:
    curr_round: Round
    pots: Pots

    def __init__(
        self, 
        curr_round: Round = None,
        pots: Pots = None
    ) -> None:
        self.curr_round = curr_round
        self.pots = pots

    def __str__(self) -> str:
        return f"{self.curr_round} {self.pots}"
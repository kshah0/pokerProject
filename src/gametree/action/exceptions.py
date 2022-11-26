from gametree.gamestate.game_state import GameState
from gametree.playerstate.player_state import PlayerState


class DefaultWinnerException(Exception):
    winner: PlayerState
    fold_state: FoldState

    def __init__(self, winner: PlayerState, fold_state: FoldState) -> None:
        self.winner = winner
        self.fold_state = fold_state

class GameEndedException(Exception):
    last_state: GameState

    def __init__(self, last_state: GameState) -> None:
        self.last_state = last_state
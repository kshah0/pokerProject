from abc import ABC, abstractmethod
from mcts.player_id import PlayerId
from mcts.game_state import GameState
from __future__ import annotations

# EXCEPTIONS

class GameEndedException(Exception):
    def __init__(self, last_state: GameState):
        self.last_state = last_state

class DefaultWinnerException(Exception):
    # TODO
    pass

class ActionWrapper(ABC):
    action: SearchBotAction

class SearchBotAction(ActionWrapper):
    game_state: GameState
    actor: PlayerId

    def __init__(self, game_state: GameState, actor: PlayerId) -> None:
        self.game_state = game_state
        self.actor = actor

    @abstractmethod
    def perform(self, context: RemoteHoldemPlayerContext) -> None:
        pass

    @abstractmethod
    def get_unwrapped_state_after_action(self) -> GameState:
        pass

    @abstractmethod
    def get_state_after_action(self) -> GameState:
        pass

    def get_new_round_state(self, last_state: GameState) -> GameState:
        next_round = last_state.get_round().get_next_round()
        if next_round is None:
            raise GameEndedException(last_state)

        new_round_state = NewRoundState(
            last_state,
            NewRoundState(
                next_round,
                Pots(last_state.get_game_pot_size()),
            )
        )

        first_to_act = new_round_state.get_next_active_player_after(new_round_state.dealer)
        if (
            (first_to_act is None) or
            new_round_state.get_next_active_player_after(first_to_act.player_id is None)
        ):
            # no one/only one player left
            return self.get_new_round_state(new_round_state)
        return NextPlayerState(new_round_state, NextPlayerEvent(first_to_act.player_id))
    
    def ends_involvement_of(self, botId: PlayerId) -> bool:
        return False
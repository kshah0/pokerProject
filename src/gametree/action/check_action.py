from gametree.action.search_bot_action import SearchBotAction
from gametree.gamestate.game_state import GameState
from gametree.gamestate.modifiers.check_state import CheckState
from gametree.gamestate.modifiers.events.check_event import CheckEvent
from gametree.gamestate.modifiers.events.next_player_event import NextPlayerEvent
from gametree.gamestate.modifiers.next_player_state import NextPlayerState
from gametree.playerstate.player_id import PlayerId
from gametree.round import Round


class CheckAction(SearchBotAction):
    def __init__(self, game_state: GameState, actor: PlayerId) -> None:
        super().__init__(game_state, actor)
    
    # @Override
    def perform(self, context: RemoteHoldemPlayerContext) -> None:
        context.check_or_call()

    # @Override
    def get_unwrapped_state_after_action(self) -> GameState:
        return CheckState(self.game_state, CheckEvent(self.actor))

    # @Override
    def get_state_after_action(self) -> GameState:
        next_to_act = self.game_state.get_next_active_player_after(self.actor)
        new_round = (
            next_to_act.has_checked() or
            self.game_state.get_round() == Round.PREFLOP or
            self.actor == self.game_state.get_big_blind() or
            self.game_state.get_largest_bet() <= self.game_state.table_config.big_blind
        )
        check_state = self.get_unwrapped_state_after_action()
        if not new_round:
            return NextPlayerState(
                check_state,
                NextPlayerEvent(next_to_act.player_id)
            )
        return self.get_new_round_state(check_state)

    def __str__(self) -> str:
        return "Check"
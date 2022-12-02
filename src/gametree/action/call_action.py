from gametree.action.search_bot_action import SearchBotAction
from gametree.gamestate.game_state import GameState
from gametree.gamestate.modifiers.all_in_state import AllInState
from gametree.gamestate.modifiers.call_state import CallState
from gametree.gamestate.modifiers.events.all_in_event import AllInEvent
from gametree.gamestate.modifiers.events.call_event import CallEvent
from gametree.gamestate.modifiers.events.next_player_event import NextPlayerEvent
from gametree.gamestate.modifiers.next_player_state import NextPlayerState
from gametree.playerstate.player_id import PlayerId
from gametree.round import Round


class CallAction(SearchBotAction):
    def __init__(self, game_state: GameState, actor: PlayerId) -> None:
        super().__init__(game_state, actor)

    def perform(self, context: RemoteHoldemPlayerContext) -> None:
        context.check_or_call()

    # @Override
    def get_unwrapped_state_after_action(self) -> GameState:
        actor_state = self.game_state.get_player(self.actor)
        largest_bet = self.game_state.get_largest_bet()
        stack = actor_state.get_stack()
        bet = actor_state.get_bet()

        if stack <= (largest_bet - bet):
            state = AllInState(
                self.game_state,
                AllInEvent(self.actor, stack)
            )
        else:
            state = CallState(
                self.game_state,
                CallEvent(self.actor, largest_bet - bet)
            )
        return state

    # @Override
    def get_state_after_action(self) -> GameState:
        round_ends = True
        players = self.game_state.get_all_seated_players()
        for player in players:
            if (
                player.is_actively_playing() and
                not player.player_id == self.actor
                and self.game_state.get_deficit(player.player_id) > 0
            ):
                round_ends = False
                break
        state = self.get_unwrapped_state_after_action()
        largest_bet = self.game_state.get_largest_bet()

        # What if small or big blind all-in?
        if (
            round_ends and
            self.game_state.get_round() == Round.PREFLOP and
            self.actor == self.game_state.get_small_blind() and
            largest_bet <= self.game_state.table_config.big_blind
        ):
            round_ends = False

        if round_ends:
            return self.get_new_round_state(state)
        else:
            next_active_player_after = state.get_next_active_player_after(self.actor)
            if next_active_player_after is None:
                return self.get_new_round_state(state)
            return NextPlayerState(
                state,
                NextPlayerEvent(next_active_player_after.player_id)
            )

    # @Override
    def __str__(self) -> str:
        return "Call"
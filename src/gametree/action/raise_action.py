from gametree.action.search_bot_action import SearchBotAction
from gametree.gamestate.game_state import GameState
from gametree.gamestate.modifiers.all_in_state import AllInState
from gametree.gamestate.modifiers.events.all_in_event import AllInEvent
from gametree.gamestate.modifiers.events.next_player_event import NextPlayerEvent
from gametree.gamestate.modifiers.next_player_state import NextPlayerState
from gametree.gamestate.modifiers.raise_state import RaiseState
from gametree.playerstate.player_id import PlayerId


class RaiseAction(SearchBotAction):
    amount: int

    def __init__(self, game_state: GameState, actor: PlayerId, amount: int) -> None:
        super().__init__(game_state, actor)
        self.amount = amount

    # @Override
    # def perform(self, context: RemoteHoldemPlayerContext) -> None:
    #     context.bet_or_raise(self.amount)

    # @Override
    def get_unwrapped_state_after_action(self) -> GameState:
        actor_state = self.game_state.get_player(self.actor)
        stack = actor_state.get_stack()
        old_bet = actor_state.get_bet()
        largest_bet = self.game_state.get_largest_bet()
        deficit = largest_bet - old_bet
        moved_amount = deficit + self.amount

        if moved_amount >= stack:
            raise_state = AllInState(
                self.game_state,
                AllInEvent(self.actor, moved_amount)
            )
        else:
            raise_state = RaiseState(
                self.game_state,
                RaiseState(self.actor, self.amount, moved_amount)
            )
        return raise_state

    # @Override
    def get_state_after_action(self) -> GameState:
        raise_state = self.get_unwrapped_state_after_action()
        return NextPlayerState(
            raise_state,
            NextPlayerEvent(
                raise_state.get_next_active_player_after(self.actor).player_id
            )
        )
    
    # @Override
    def __str__(self) -> str:
        actor_state = self.game_state.get_player(self.actor)
        stack = actor_state.get_stack()
        old_bet = actor_state.get_bet()
        largest_bet = self.game_state.get_largest_bet()
        deficit = largest_bet - old_bet
        moved_amount = deficit + self.amount

        if moved_amount >= stack:
            return f"Raise {self.amount} (all-in)"
        return f"Raise {self.amount}"
from gametree.action.search_bot_action import SearchBotAction
from gametree.gamestate.game_state import GameState
from gametree.playerstate.player_id import PlayerId


class BetAction(SearchBotAction):
    amount: int

    def __init__(self, game_state: GameState, actor: PlayerId, amount: int) -> None:
        super().__init__(game_state, actor)
        self.amount = amount

    # @Override
    def perform(self, context: RemoteHoldemPlayerContext) -> None:
        context.bet_or_raise(self.amount)

    # @Override
    def get_unwrapped_state_after_action(self) -> GameState:
        stack = self.game_state.get_player(self.actor).get_stack()
        if stack == self.amount:
            bet_state = AllInState(
                self.game_state,
                AllInEvent(self.actor, self.amount)
            )
        elif stack > amount:
            bet_state = BetState(
                self.game_state,
                BetEvent(self.actor, self.amount)
            )
        else:
            raise ValueError(f"Can't bet amount {self.amount} with stack {stack}")
        return bet_state
    
    # @Override
    def get_state_after_action(self) -> GameState:
        bet_state = self.get_unwrapped_state_after_action()
        next_to_act = bet_state.get_next_active_player_after(self.actor)
        if next_to_act is not None:
            return NextPlayerState(
                bet_state,
                NextPlayerEvent(next_to_act.player_id)
            )
        raise RuntimeError("Round can't be over after a bet")

    def __str__(self) -> str:
        if self.game_state.get_player(self.actor).get_stack() == self.amount:
            return f"Bet {self.amount} (all in)"
        return f"Bet {self.amount}"
        
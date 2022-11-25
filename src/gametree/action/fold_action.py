from gametree.action.exceptions import DefaultWinnerException
from gametree.action.search_bot_action import SearchBotAction
from gametree.mcts.game_state import GameState
from gametree.mcts.player_id import PlayerId


class FoldAction(SearchBotAction):
    def __init__(self, game_state: GameState, actor: PlayerId) -> None:
        super().__init__(game_state, actor)

    # @Override
    def perform(self, context: RemoteHoldemPlayerContext) -> None:
        context.fold()

    # @Override
    def get_unwrapped_state_after_action(self) -> GameState:
        return FoldState(self.game_state, FoldEvent(self.actor))

    # @Override
    def get_state_after_action(self) -> GameState:
        round_ends = True
        players = self.game_state.get_all_seated_players()
        first = None
        no_default_winner = False
        for player in players:
            if (
                round_ends and player.is_actively_playing() and
                not player.player_id == self.actor and
                self.game_state.get_deficit(player.player_id) > 0
            ):
                round_ends = False
            if (
                not no_default_winner and
                not player.player_id == self.actor
            ):
                if first is not None:
                    no_default_winner = True
                else:
                    first = player
            if no_default_winner and not round_ends:
                break
        if not no_default_winner:
            raise DefaultWinnerException(
                first,
                FoldState(self.game_state, FoldEvent(self.actor))
            )
        if (
            round_ends and
            self.game_state.round == Round.PREFLOP and
            self.actor == self.game_state.get_small_blind() and
            self.game_state.get_largest_bet() <= self.game_state.table_config.big_blind
        ):
            round_ends = False
        
        fold_state = self.get_unwrapped_state_after_action()

        if not round_ends:
            return NextPlayerState(
                fold_state,
                NextPlayerEvent(
                    fold_state.get_next_active_player_after(self.actor).player_id
                )
            )
        return self.get_new_round_state(fold_state)
        
    # @Override
    def ends_involvement_of(self, bot_id: PlayerId) -> bool:
        return self.actor == bot_id
        
    # @Override
    def __str__(self) -> str:
        return "Fold"
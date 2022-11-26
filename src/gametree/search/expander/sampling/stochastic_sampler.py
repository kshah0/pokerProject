from abc import ABC, abstractmethod
from typing import List
from gametree.action.bet_action import BetAction
from gametree.action.call_action import CallAction
from gametree.action.check_action import CheckAction
from gametree.action.fold_action import FoldAction
from gametree.action.probability_action import ProbabilityAction
from gametree.action.raise_action import RaiseAction
from gametree.gamestate.game_state import GameState
from gametree.playerstate.player_id import PlayerId
from gametree.search.expander.sampling.sampler import Sampler


class StochasticSampler(Sampler, ABC):
    num_bet_size_samples: int

    def __init__(self, num_bet_size_samples: int = 5) -> None:
        self.num_bet_size_samples = num_bet_size_samples

    def get_probability_actions(self, game_state: GameState, model: OpponentModel, actor: PlayerId, bot: PlayerId) -> List[ProbabilityAction]:
        actions = []
        total_probability = 0.0
        if game_state.get_deficit(actor) > 0:
            # call, raise, or fold
            # 3-element tuple
            probabilities = model.get_fold_call_raise_probabilities(game_state, actor)

            fold_probability = probabilities[0]
            total_probability += fold_probability
            actions.append(
                ProbabilityAction(
                    FoldAction(game_state, actor),
                    fold_probability
                )
            )

            call_probability = probabilities[1]
            total_probability += call_probability
            actions.append(
                ProbabilityAction(
                    CallAction(game_state, actor),
                    call_probability
                )
            )

            if (
                not game_state.get_player(bot).is_all_in() and
                game_state.is_allowed_to_raise(actor)
            ):
                raise_probability = probabilities[2]
                lower_raise_bound = game_state.get_lower_raise_bound(actor)
                upper_raise_bound = game_state.get_upper_raise_bound(actor)
                bet_size_samples = self.get_stochastic_samples(self.num_bet_size_samples)
                for bet_size_sample in bet_size_samples:
                    bet_action = RaiseAction(
                        game_state,
                        actor,
                        int(round(lower_raise_bound + bet_size_sample * (upper_raise_bound - lower_raise_bound)))
                    )
                    actions.append(ProbabilityAction(bet_action, raise_probability/self.num_bet_size_samples))
                    total_probability += raise_probability / self.num_bet_size_samples
        else:
            # check or bet
            probabilities = model.get_check_bet_probabilities(game_state, actor)
            check_probability = probabilities[0]
            total_probability += check_probability

            actions.append(
                ProbabilityAction(
                    CheckAction(game_state, actor),
                    check_probability
                )
            )

            if (
                not game_state.get_player(bot).is_all_in() and
                game_state.is_allowed_to_raise(actor)
            ):
                bet_probability = probabilities[1]
                lower_raise_bound = game_state.get_lower_raise_bound(actor)
                upper_raise_bound = game_state.get_upper_raise_bound(actor)
                bet_size_samples = self.get_stochastic_samples(self.num_bet_size_samples)
                for bet_size_sample in bet_size_samples:
                    bet_action = BetAction(
                        game_state,
                        actor,
                        int(round(lower_raise_bound + bet_size_sample * (upper_raise_bound - lower_raise_bound)))
                    )
                    actions.append(ProbabilityAction(bet_action, bet_probability/self.num_bet_size_samples))
                    total_probability += bet_probability / self.num_bet_size_samples
        return actions

    @abstractmethod
    def get_stochastic_samples(self, n: int) -> List[float]:
        pass
                
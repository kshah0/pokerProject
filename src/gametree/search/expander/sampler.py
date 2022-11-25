from abc import ABC, abstractmethod
from typing import List
from action.probability_action import ProbabilityAction
from gametree.action.bet_action import BetAction
from gametree.action.raise_action import RaiseAction
from mcts.game_state import GameState

from mcts.player_id import PlayerId


class Sampler(ABC):

    @abstractmethod
    def get_probability_actions(
        self,
        game_state: GameState,
        model: OpponentModel,
        actor: PlayerId,
        bot: PlayerId,
    ):
        pass

    def add_raise_probabilities(
        self,
        game_state: GameState,
        actor: PlayerId,
        actions: List[ProbabilityAction],
        raise_probability: float,
        raised: bool,
        relative_bet_size_samples: List[float],
        relative_p_bet_size_samples: List[float],
    ):
        lower_raise_bound = game_state.get_lower_raise_bound(actor)
        upper_raise_bound = game_state.get_upper_raise_bound(actor)
        if lower_raise_bound < upper_raise_bound:
            temp_amount = 0
            temp_probability = 0
            for i in range(len(relative_bet_size_samples)):
                probability = raise_probability*relative_p_bet_size_samples[i]
                amount = lower_raise_bound + (
                    upper_raise_bound - lower_raise_bound
                )*relative_bet_size_samples[i]
                small_blind = game_state.get_table_configuration().get_small_blind()
                amount_int = min(int(small_blind*round(amount/small_blind), upper_raise_bound))
                temp_probability += probability
                if abs(temp_amount - amount_int) >= 2*small_blind:
                    temp_amount = amount_int
                    if amount_int < lower_raise_bound:
                        amount_int += small_blind
                    if amount_int > upper_raise_bound:
                        amount_int = upper_raise_bound
                    if raised:
                        actions.add(
                            ProbabilityAction(
                                RaiseAction(
                                    game_state,
                                    actor,
                                    amount_int
                                ),
                                temp_probability
                            )
                        )
                    else:
                        actions.add(
                            ProbabilityAction(
                                BetAction(
                                    game_state,
                                    actor,
                                    amount_int
                                ),
                                temp_probability
                            )
                        )
                    temp_probability = 0.0
        elif raised:
            actions.add(
                ProbabilityAction(
                    RaiseAction(
                        game_state,
                        actor,
                        lower_raise_bound
                    ),
                    raise_probability
                )
            )
        else:
            actions.add(
                ProbabilityAction(
                    BetAction(
                        game_state,
                        actor,
                        lower_raise_bound
                    ),
                    raise_probability
                )
            )
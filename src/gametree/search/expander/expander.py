from typing import List
from action.probability_action import ProbabilityAction
from search.expander.sampler import Sampler
from mcts.player_id import PlayerId


from mcts.game_state import GameState
class Expander:
    num_bet_size_samples: int
    game_state: GameState
    actor: PlayerId
    bot: PlayerId
    sampler: Sampler
    model: OpponentModel

    def __init__(
        self,
        game_state: GameState,
        model: OpponentModel,
        actor: PlayerId,
        bot: PlayerId,
        sampler: Sampler,
    ) -> None:
        self.game_state = game_state
        self.actor = actor
        self.bot = bot
        self.sampler = sampler
        self.model = model

    def get_probability_actions(self) -> List[ProbabilityAction]:
        return self.sampler.get_probability_actions(self.game_state, self.model, self.actor, self.bot)

    # class Factory(ABC):

    #     @abstractmethod
    #     def create(
    #         self,
    #         node: InnerGameTreeNode,
    #         tokens: int,
    #         sampler: Sampler,
    #     )
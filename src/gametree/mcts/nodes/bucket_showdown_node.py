from action.probability_action import ProbabilityAction
from gametree.gamestate.game_state import GameState
from mcts.nodes.inner_node import InnerNode
from mcts.nodes.showdown_node import ShowdownNode

from __future__ import annotations


class MCTSBucketShowdownNode(ShowdownNode):

    rollout: BucketRollout
    stack_size: int

    def __init__(self, game_state: GameState, parent: InnerNode, last_action: ProbabilityAction) -> None:
        super().__init__(parent, last_action)
        self.rollout = BucketRollout(game_state, parent.bot)
        self.stack_size = self.rollout.botState.get_stack()
        self.game_state = self.rollout.game_state

    def simulate(self) -> float:
        return self.stack_size + self.rollout.do_rollout(4)

    class Factory(ShowdownNode.Factory):

        # @Override
        def create(self, game_state: GameState, parent: InnerNode, prob_action: ProbabilityAction) -> MCTSBucketShowdownNode:
            return MCTSBucketShowdownNode(game_state, parent, prob_action)
from action.probability_action import ProbabilityAction
from gametree.gamestate.game_state import GameState
from mcts.nodes.config import Config
from mcts.nodes.inner_node import InnerNode
from mcts.nodes.inode import INode
from gametree.playerstate.player_id import PlayerId
from mcts.strategies.backpropagation.backpropagation_strategy import BackPropagationStrategy


class DecisionNode(InnerNode):
    def __init__(self, parent: InnerNode, prob_action: ProbabilityAction, game_state: GameState, bot: PlayerId, config: Config):
        super().__init__(parent, prob_action, game_state, bot, config)

    # @Override
    def select_child(self) -> INode:
        return self.config.decision_node_selection_strat.select(self)

    # @Override
    def create_back_prop_strategy(self) -> BackPropagationStrategy:
        return self.config.backpropagation_strat_factory.create_for_decision_node(self)
from gametree.gamestate.game_state import GameState
from gametree.mcts.nodes.config import Config
from gametree.mcts.nodes.decision_node import DecisionNode
from gametree.playerstate.player_id import PlayerId


class RootNode(DecisionNode):
    def __init__(self, game_state: GameState, bot: PlayerId, config: Config):
        super().__init__(None, None, game_state, bot, config)
        self.config.model.assume_permanently(game_state)
        self.expand_children()

    # @Override
    def backpropagate(self, value: float) -> None:
        self.back_prop_strategy.on_back_propagate(value)
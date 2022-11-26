from gametree.search.expander.sampling.sampler import Sampler
from mcts.nodes.showdown_node import ShowdownNode
from mcts.strategies.backpropagation.backpropagation_strategy import BackPropagationStrategy
from mcts.strategies.selection.selection_strategy import SelectionStrategy


class Config:
    showdown_node_factory: ShowdownNode.Factory
    model: OpponentModel
    decision_node_selection_strat: SelectionStrategy
    opponent_node_selection_strat: SelectionStrategy
    move_selection_strat: SelectionStrategy
    backpropagation_strat_factory: BackPropagationStrategy.Factory
    sampler: Sampler

    def __init__(
        self,
        model: OpponentModel,
        showdown_node_factory: ShowdownNode.Factory,
        decision_node_selection_strat: SelectionStrategy,
        opponent_node_selection_strat: SelectionStrategy,
        move_selection_strat: SelectionStrategy,
        backpropagation_strat_factory: BackPropagationStrategy.Factory,
        sampler: Sampler,
    ) -> None:
        self.model = model
        self.showdown_node_factory = showdown_node_factory
        self.decision_node_selection_strat = decision_node_selection_strat
        self.opponent_node_selection_strat = opponent_node_selection_strat
        self.move_selection_strat = move_selection_strat
        self.backpropagation_strat_factory = backpropagation_strat_factory
        self.sampler = sampler
from abc import abstractmethod
import random
from typing import List
from gametree.action.exceptions import DefaultWinnerException, GameEndedException
from mcts.nodes.config import Config
from mcts.nodes.constant_leaf_node import ConstantLeafNode
from mcts.nodes.decision_node import DecisionNode
from search.expander.expander import Expander
from mcts.nodes.opponent_node import OpponentNode
from mcts.player_id import PlayerId
from action.probability_action import ProbabilityAction
from mcts.game_state import GameState
from mcts.nodes.inode import INode
from __future__ import annotations

from mcts.strategies.backpropagation.backpropagation_strategy import BackPropagationStrategy
from mcts.strategies.selection.selection_strategy import SelectionStrategy

class InnerNode(INode):
    # Inherited from INode
    # parent: InnerNode
    # last_action: ProbabilityAction
    # game_state: GameState

    config: Config
    probabilities: List[float]
    cumulative_probability: List[float]
    children: List[INode]
    back_prop_strategy: BackPropagationStrategy
    bot: PlayerId

    def __init__(
        self,
        parent: InnerNode,
        prob_action: ProbabilityAction,
        game_state: GameState,
        bot: PlayerId,
        config: Config,
    ):
        self.parent = parent
        self.last_action = prob_action
        self.bot = bot
        self.game_state = game_state
        self.config = config
        self.back_prop_strategy = self.create_back_prop_strategy()

    @abstractmethod
    def create_back_prop_strategy(self) -> BackPropagationStrategy:
        pass

    @abstractmethod
    def select_child(self) -> INode:
        pass

    def select_recursively(self) -> INode:
        needs_child_expansion = (len(self.children) == 0)
        if needs_child_expansion:
            self.config.model.assume_temporarily(self.game_state)
            self.expand_children()
        selected_child = self.select_child().select_recursively()
        if needs_child_expansion:
            self.config.model.forgetLastAssumption()
        return selected_child

    # selectChild(SelectionStrategy selectionStrategy)
    def select_child_using_strategy(self, selection_strategy: SelectionStrategy):
        return selection_strategy.select(self)

    # @Override
    def expand(self) -> None:
        return

    def simulate(self) -> float:
        raise RuntimeError("Tried to select non-leaf node")

    def get_random_child(self) -> INode:
        random_number = random.random()
        for i in range(len(self.cumulative_probability)-1):
            if random_number < self.cumulative_probability[i]:
                return self.children[i]
        return self.children[len(self.cumulative_probability)-1]

    def backpropagate(self, value: float) -> None:
        self.back_prop_strategy.on_back_propagate(value)
        self.parent.backpropagate(value)

    # @Override
    def get_EV(self) -> float:
        return self.back_prop_strategy.get_EV()

    # @Override
    def get_num_samples(self) -> int:
        return self.back_prop_strategy.get_num_samples()

    # @Override
    def get_std_dev(self) -> float:
        return self.back_prop_strategy.get_std_dev()

    # @Override
    def get_EV_variance(self) -> float:
        return self.back_prop_strategy.get_EV_variance()

    # @Override
    def get_EV_std_dev(self) -> float:
        return self.back_prop_strategy.get_EV_std_dev()

    # @Override
    def get_variance(self) -> float:
        return self.back_prop_strategy.get_variance()

    # @Override
    def get_num_samples_in_mean(self) -> int:
        return self.back_prop_strategy.get_num_samples_in_mean()

    def expand_children(self) -> None:
        if len(self.children) == 0:
            expander = Expander(
                self.game_state, 
                self.config.model,
                self.game_state.get_next_to_act(),
                self.bot,
                self.config.sampler,
            )
            actions = expander.get_probability_actions()
            self.probabilities = []
            self.cumulative_probability = []
            cumul = 0
            for action in actions:
                probability = action.get_probability()
                cumul += probability
                self.probabilities.append(probability)
                self.cumulative_probability.append(cumul)
                self.children.append(self.get_child_after(action))

    def get_child_after(self, prob_action: ProbabilityAction) -> INode:
        action = prob_action.get_action()
        if action.ends_involvement_of(self.bot):
            # bot folded
            return ConstantLeafNode(
                self, 
                prob_action,
                self.game_state.get_player(self.bot).get_stack(),
            )
        try:
            next_state = action.get_state_after_action()
            # expand further
            if next_state.get_next_to_act() == self.bot:
                return DecisionNode(
                    self,
                    prob_action,
                    next_state,
                    self.bot,
                    self.config,
                )
            else:
                return OpponentNode(
                    self,
                    prob_action,
                    next_state,
                    self.bot,
                    self.config,
                )
        except GameEndedException as e:
            return self.config.showdown_node_factory.create(
                    e.last_state, 
                    self, 
                    prob_action
                )
        except DefaultWinnerException as e:
            # assert e.winner.get_player_id() == self.bot
            return ConstantLeafNode(
                self,
                prob_action,
                self.game_state.get_player(self.bot).get_stack() + int(
                    e.fold_state.get_game_pot_size()*(1-self.game_state.get_table_configuration().get_rake())
                )
            )

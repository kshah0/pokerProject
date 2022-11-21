import copy
import random
import time
from typing import Dict
from game_state import is_over, next_moves
from node import (
    PokerMove,
    PokerGameState,
    Node,
    NodeType,
)
from __future__ import annotations

def construct_search_tree(
    game_state: PokerGameState,
    strategies: Dict[NodeType, function], # Pass in a dictionary with different selection strategy for each node type
    T: float = 1,
)-> Node:
    start_time = time.time()
    # Create a root node
    root = Node(game_state)
    # Loop until no more time
    while time.time() - start_time < T:
        leaf = find_leaf(root, strategies)
        over, result = is_over(leaf.game_state)
        if over:
            backpropagate(leaf, result)
        else:
            # Not over yet, so add a new child (via rejection sampling) at random.
            moves = next_moves(leaf.game_state)
            move = random.choice(moves)
            while move in leaf.children.keys():
                move = random.choice(moves)
            child = Node(
                game_state=copy.deepcopy(leaf.game_state),
                parent=leaf,
            )
            leaf.children[move] = child

            update_game_state(child.game_state, move)

            # Simulate until a terminal state
            result = simulate(child)

            # Backpropagate
            backpropagate(child, result)
    return root

def find_leaf(
    root: Node,
    strategies: Dict[NodeType, function],
) -> Node:
    if (
        len(root.children) < len(next_moves(root.game_state))
        or
        is_over(root.game_state)[0]
    ):
        return root
    return find_leaf(strategies[root.node_type](root), strategies)

def simulate(root: Node):
    current_game_state = root.game_state
    while True:
        over, result = is_over(current_game_state)
        if over:
            return result
        next_move = random.choice(next_moves(current_game_state))
        new_game_state = copy.deepcopy(current_game_state)

        update_game_state(new_game_state, next_move)

        current_game_state = new_game_state

def backpropagate(
    node: Node,
    result: float,
):
    node.total_value += result
    node.num_episodes += 1
    backpropagate(node.parent, result)

def update_game_state(
    game_state: PokerGameState,
    move: PokerMove,
):
    pass
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log, inf

num_nodes = 1000
explore_faction = 2.0


def traverse_nodes(node, board, state, identity):
    """Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.
    """
    # print("curr_state: ", state)

    act_list = node.untried_actions
    our_board_bool = state[-1] == identity
    # print("our board: ", our_board_bool)

    if len(act_list) > 0 or board.is_ended(state):
        return node
    else:
        best_val = float("-inf")
        best_act = list(node.child_nodes.keys())[0]
        # print("best_act: ", best_act)
        best_node = node.child_nodes[best_act]
        # best_val = 0 - 9999

        # print("all child: ", node.child_nodes.items())
        for curr_act, curr_node in node.child_nodes.items():
            child_win_rate = curr_node.wins
            if not our_board_bool:
                child_win_rate = 1 - child_win_rate
            curr_val = (child_win_rate / curr_node.visits) + explore_faction * sqrt(
                log(node.visits) / child_win_rate
            )

            if curr_val > best_val:
                best_val = curr_val
                best_act = curr_act
                best_node = curr_node

        new_state = board.next_state(state, best_act)

        return traverse_nodes(best_node, board, new_state, identity)


def expand_leaf(node, board, state):
    """Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """

    # you can call rollout in this function
    curr_action = choice(node.untried_actions)
    new_state = board.next_state(state, curr_action)
    legal_acts = board.legal_actions(new_state)

    tmp_leaf = MCTSNode(node, curr_action, legal_acts)
    return tmp_leaf
    # pass
    # Hint: return new_node


def rollout(board, state):
    """Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    end_bool = board.is_ended(state)
    if not end_bool:
        rand_act = choice(board.legal_actions(state))
        next_state = board.next_state(state, rand_act)
        return rollout(board, next_state)

    return state
    # pass


def backpropagate(node, won):
    """Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.
    """

    node.wins += won
    node.visits += 1
    if node.parent != None:
        backpropagate(node.parent, node.wins)
    # pass


def think(board, state):
    """Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    # an_Act =
    root_node = MCTSNode(
        parent=None, parent_action=None, action_list=board.legal_actions(state)
    )

    # leaf_node = traverse_nodes(root_node, board, state, identity_of_bot)
    # print(f"leaf_node.parent_action = {leaf_node.parent_action}")
    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        # print("step: ", step)
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        tmp_node = traverse_nodes(node, board, sampled_game, identity_of_bot)
        tmp_leaf = expand_leaf(tmp_node, board, sampled_game)
        tmp_state = rollout(board, sampled_game)
        win_vals = board.points_values(tmp_state)
        backpropagate(tmp_leaf, win_vals[identity_of_bot])
        node.child_nodes[tmp_leaf.parent_action] = tmp_leaf

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.

    # most_visits = float("-inf")
    most_wins = float("-inf")
    best_act = None
    for curr_act, curr_child in root_node.child_nodes.items():
        if curr_child.wins > most_wins:
            best_act = curr_act

    return best_act

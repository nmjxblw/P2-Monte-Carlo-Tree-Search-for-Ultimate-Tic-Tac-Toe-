from mcts_node import MCTSNode
from random import choice
from math import sqrt, log, inf

num_nodes = 200
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
    our_board_bool = identity == board.current_player(state)
    # print("our board: ", our_board_bool)

    if board.is_ended(state) or len(act_list) > 0:
        return (node, state)
    else:
        # print("curr node: ", node)
        # best_val = float("-inf")
        best_val = 0 - 9999
        best_act = list(node.child_nodes.keys())[0]
        best_node = node.child_nodes[best_act]

        for curr_act, curr_node in node.child_nodes.items():
            # print("curr child: ", curr_node)
            child_win_rate = curr_node.wins / curr_node.visits
            if not our_board_bool:
                child_win_rate = 1 - child_win_rate
            curr_val = (child_win_rate) + explore_faction * sqrt(
                log(node.visits) / curr_node.visits
            )
            if curr_val > best_val:
                best_val = curr_val
                best_act = curr_act
                best_node = curr_node
        new_state = board.next_state(state, best_act)
        # print("new state: ", new_state)
        return (best_node, new_state)

        # return traverse_nodes(best_node, board, new_state, identity)


def expand_leaf(node, board, state):
    """Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """

    # you can call rollout in this function
    if len(node.untried_actions) < 1:
        return (node, state)

    curr_action = choice(node.untried_actions)
    node.untried_actions.remove(curr_action)
    new_state = board.next_state(state, curr_action)
    legal_acts = board.legal_actions(new_state)

    tmp_leaf = MCTSNode(node, curr_action, legal_acts)
    node.child_nodes[curr_action] = tmp_leaf
    return (tmp_leaf, new_state)
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

    # print("won val: ", won)
    node.wins += won
    node.visits += 1
    if node.parent != None:
        backpropagate(node.parent, won)
    # pass


def think(board, state):
    """Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(
        parent=None, parent_action=None, action_list=board.legal_actions(state)
    )

    # leaf_node = traverse_nodes(root_node, board, state, identity_of_bot)
    # print(f"leaf_node.parent_action = {leaf_node.parent_action}")
    for step in range(num_nodes):
        # print("step: ", step)
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        tmp_node = traverse_nodes(node, board, sampled_game, identity_of_bot)
        tmp_leaf = expand_leaf(tmp_node[0], board, tmp_node[1])
        tmp_state = rollout(board, tmp_leaf[1])
        win_vals = board.points_values(tmp_state)
        # print("win vals: ", win_vals)
        # win_vals = board.win_values(tmp_state)
        backpropagate(tmp_leaf[0], win_vals[identity_of_bot])

        # print("untried list: ", node.untried_actions)

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.

    most_wins = 0 - 9999
    best_act = None
    for curr_act, curr_child in root_node.child_nodes.items():
        # print("most wins: ", most_wins)
        # if curr_child.wins > most_wins or curr_child.visits > most_visits:
        curr_val = curr_child.wins / curr_child.visits
        if curr_val > most_wins:
            # print("child wins: ", curr_child.wins)
            # print("child visits: ", curr_child.visits)
            most_wins = curr_val
            # most_visits = curr_child.visits
            best_act = curr_act

    return best_act

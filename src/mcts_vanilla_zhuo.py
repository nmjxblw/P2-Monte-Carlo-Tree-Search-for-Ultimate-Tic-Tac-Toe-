from mcts_node import MCTSNode
from random import choice
from math import sqrt, log, inf
import os

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

    if len(node.untried_actions) > 0 or board.is_ended(state):
        # the first idea is to check if there is any untrid action for this node
        # if the node does have at least one untried action
        # elif the game is over
        # we dont have to do search any more
        # return it
        return node

    elif len(node.child_nodes.keys()) == 1:
        # if the node has only one child
        # return the child
        action = list(node.child_nodes.keys()).pop()
        # update the state
        new_state = board.next_state(state, action)
        # we go to the unique child
        return traverse_nodes(node.child_nodes[action], board, new_state, identity)
    else:
        # in this condition, node has at least 2 child_nodes
        # and the node doesn't have any untried_actions
        # then we need to get the UCT value to find the best child node
        best_node = None
        best_action = None
        best_val = -inf
        worse_val= inf


        for action in node.child_nodes.keys():
            # action is the key to get the child node
            temp_node = node.child_nodes[action]
            try:
                # try to get Upper Confidence Bound for Trees(UCT) value
                win_rate = temp_node.wins / temp_node.visits
                if 3 - state[-1] != identity:
                    win_rate = 1 - win_rate
                uct_val = win_rate + explore_faction * sqrt(
                    log(node.visits) / temp_node.visits
                )
                # if we get the UCT value
                # compare with the best value
                if best_val < uct_val and 3 - state[-1] == identity:
                    # if we find the bigger value
                    # update the best value and the best node, also the best action
                    best_val = uct_val
                    best_node = temp_node
                    best_action = action
                elif worse_val > uct_val and 3 - state[-1] != identity:
                    worse_val = uct_val
                    best_node = temp_node
                    best_action = action

            except ZeroDivisionError:
                # this means 0 visits in this child node
                # need to update its inside information
                # so we return this node
                return temp_node
        # we pick up the best action, then we need to update state
        if best_action == None:
            return node.parent
        new_state = board.next_state(state, best_action)
        # and then the best child node become parent node
        #
        return traverse_nodes(best_node, board, new_state, identity)


def expand_leaf(node, board, state):
    """Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """

    if len(node.untried_actions) > 0:
        # this means it has untried_actions
        # update the state
        action = node.untried_actions.pop()
        new_state = board.next_state(state, action)
        # make a new MCTSNode
        new_node = MCTSNode(
            parent=node,
            parent_action=action,
            action_list=board.legal_actions(new_state),
        )
        # set new_node as a child of node
        node.child_nodes[action] = new_node
       
        return new_node
    else:
        # untried_actions is empty
        # its no possible to add a leaf
        # update the information of the tree
        # backpropagate(node,0)
        return node


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
    # update the informations inside the node
    node.wins += won
    node.visits += 1
    # checking if the current node is the root
    if node.parent == None:
        return
    else:
        # recursion
        return backpropagate(node.parent, won)
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
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        # pick a node
        node = traverse_nodes(node, board, sampled_game, identity_of_bot)
        leaf_node = expand_leaf(node, board, sampled_game)
        sampled_game = board.next_state(sampled_game, leaf_node.parent_action)
        sampled_game = rollout(board, sampled_game)
        won = board.points_values(sampled_game)[identity_of_bot]
        backpropagate(leaf_node, won)

    # we finished building the tree
    factor = -inf
    best_action = None
    for action in root_node.child_nodes.keys():
        if (
            factor
            < root_node.child_nodes[action].wins + root_node.child_nodes[action].visits
        ):
            factor = (
                root_node.child_nodes[action].wins
                - root_node.child_nodes[action].visits
            )
            best_action = action
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return best_action

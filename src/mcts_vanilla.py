
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    legal_board_act = board.legal_actions(state)
    leaf_node  = {}
    nodes = node.keys()
    while  nodes:
        child = nodes.pop()
        if child.child_nodes == {}:
            # find a leaf node
            # checking if child's action are legal
            for curr_action in child.untried_actions:
                if curr_action in legal_board_act:
                    # push it into the dict
                    leaf_node[child] = None
        else:
            # not a leaf node
            # push the children of the node into the list
            nodes += node.keys()

    # Hint: return leaf_node
    return  leaf_node


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """

    
    # Hint: return new_node

    curr_node = node
    curr_node_action = node.action
    chilen_of_curr_node_action_list = curr_node.untried_action
    new_node = MCTSNode(parent, parent_action, action_list)
    new_node.parent.child_nodes[new_node] = None
    return 

def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    # pass
    # maybe a solution
    return choice(board.legal_actions(state))


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    if node.parent == None:
        return
    else:
        node.wins += won
        node.visits += 1
        backpropagate(node.parent,won)


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!

        # 1.Selection
        # get childen 
        for node_acation in node.untried_actions:
            if board.is_legal(board,node_acation):
               node = expand_leaf(node,board,state)
               node.parent_action = node_acation

        # leaf_nodes = traverse_nodes(node, board, state, identity_of_bot)
        # 2.Expansion
        # 3.Simulation
        # 4.Backpropagation
        # root_node = best_node

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return action

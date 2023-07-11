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
    # own_boxes = board.owned_boxes(state).values()
   

   
    
    if len(node.untried_actions) > 0:
        # the first idea is to check if there is any untrid action for this node
        # if the node does have at least one untried action
        # return it
        return node
    
    elif len(node.child_nodes.keys()) == 1:
        # if the node has only one child
        # return the child
        action = node.child_nodes.keys().pop()
        return traverse_nodes(node.child_nodes[action],board, state, identity)
    else:
        # else we do the UCT to find the best child node
        return_node = None
        best_val = -inf

        for action in node.child_nodes.keys():
            return_node = node.child_nodes[aciton]
            try:
                uct_val = temp_node.wins/temp_node.visits + explore_faction * sqrt(node.visits / temp_node.visits)
            except ZeroDivisionError:
                # this means 0 visits in child node
                return return_node


    # return_node = node
    # curr_state = state
    # while len(node.untried_actions) > 0:
    #     action = node.untried_actions.pop()
    #     # update the child_node
    #     # 1.get the next state
    #     temp_state = board.next_state(state, action)
    #     # 2.get information of child and set as a MCTSNode
    #     #   get parent & parent_action & legal_action
    #     # 3.using the action as a key to store the MCTSNode
    #     node.child_nodes[action] = MCTSNode(
    #         parent=node,
    #         parent_action=action,
    #         action_list=board.legal_actions(temp_state),
    #     )

    # if not parent_acts.isEmpty():
    # if not board.is_ended(curr_state):
    #     act_list = return_node.untried_actions
    #     print("curr state: ", curr_state)
        # print("curr node children: ", return_node.child_nodes.keys())

        """
        checking if a node has en empty untried_list
        if so, then we make one of it's children into the next
        leaf node
        """
        # if len(act_list) == 1:
            # this means the node has only 1 child
            # so we just have to return the child node
            # that is good enough
            # curr_act = act_list[0]
            # new_state = board.next_state(curr_state, curr_act)
            # print("new state: ", new_state)
            # new_untried_actions = board.legal_actions(new_state)
            # tmp_leaf = expand_leaf(return_node, board, new_state)
            # return_node.child_nodes[curr_act] = tmp_leaf

            # return tmp_leaf

        # else, that means we can still traverse the tree
        # till we hit a node with an empty untried_list
        # by choosing the best node by it's value through the
        # current node's children
        # elif len(act_list) > 1:
            # if num of children is greater than 2
            # do UCT to find out the best child

    #         best_val = float("-inf")
    #         best_node = None
    #         best_act = None
    #         parent_visits = return_node.visits

    #         for curr_act, curr_child in return_node.child_nodes.items():
    #             new_state = board.next_state(curr_state, curr_act)
    #             num_visits = curr_child.visits
    #             if (
    #                 board.owned_boxes(new_state)[curr_act] == identity
    #                 and num_visits > 0
    #             ):
    #                 print("curr act: ", curr_act)
    #                 num_visits = curr_child.visits
    #                 num_wins = curr_child.wins
    #                 exploit = num_visits / num_wins
    #                 new_strat = (log(parent_visits)) / num_visits
    #                 sqrt_strat = sqrt(new_strat)
    #                 sqrt_strat *= explore_faction
    #                 new_val = exploit + sqrt_strat

    #                 # checking if the current child node's value is
    #                 # the best value to choose
    #                 if new_val > best_val:
    #                     best_val = new_val
    #                     best_node = curr_child
    #                     best_act = curr_act

    #                 return_node = best_node

    #         print("best act: ", best_act)
    #         # curr_state = board.next_state(curr_state, best_act)
    #         if return_node == None:
    #             return_node = node.child_nodes[choice(node.child_nodes.keys())]

    # return return_node
    # Hint: return leaf_node


def expand_leaf(node, board, state):
    """Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    act_list = node.untried_actions
    curr_action = act_list[0]
    legal_acts = board.legal_actions(state)

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
        next_state = board.next_State(state, rand_act)
        return rollout(board, next_state)

    # while not end_bool:
    #     rand_act = choice(board.legal_actions(state))
    #     state = board.next_state(state, rand_act)
    #     end_bool = board.is_ended(state)

    return
    # pass


def backpropagate(node, won):
    """Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    # checking if the current node is the root
    if node.parent == None:
        return
    else:
        # else, we just do our checks and update the node
        # if player has 3 ways to win in this way, we sign won as -3
        # but if bot also has 1 way to win in this way, won = -3 + 1 = -2
        node.wins += won
        node.visits += 1
        return backpropagate(node.parent, node.parent.wins)
    # pass


def think(board, state):
    """Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    print("Identity: ", identity_of_bot)
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
        node = traverse_nodes(node, board, sampled_game, identity_of_bot)

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return None

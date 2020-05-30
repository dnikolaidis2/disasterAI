from .move import MoveType
from .globals import getOtherSide


def minimax(node, depth, maximizing_player, a, b, ab_switch, q_search, in_danger, en_masse):
    # What makes a node Terminal?
    if node.is_terminal():
        return node.state_evaluation(in_danger, en_masse)

    if depth == 0:
        if q_search:
            return qsearch(node, maximizing_player, in_danger, en_masse)
        else:
            return node.state_evaluation(in_danger, en_masse)

    if maximizing_player:
        value = -100000

        for child in node.successor_states():
            value = max(value, minimax(child, depth-1, False, a, b, ab_switch, q_search, in_danger, en_masse))
            a = max(value, a)
            if a >= b and ab_switch:
                break 

        return value
    
    else:
        value = +100000

        for child in node.successor_states():
            value = min(value, minimax(child, depth-1, True, a, b, ab_switch, q_search, in_danger, en_masse))
            b = min(b, value)
            if a >= b and ab_switch:
                break
        
        return value


def qsearch(node, maximizing_player, in_danger, en_masse):
    stat_eval = node.state_evaluation(in_danger, en_masse)
    if node.move.type == MoveType.JUMP:
        node.set_color(getOtherSide(node.color))
        for state in node.successor_states():
            if state.move.type == MoveType.JUMP:
                if state.move.jump_count > node.move.jump_count:
                    if maximizing_player:
                        return -500
                    else:
                        return 500
                else:
                    return stat_eval
            else:
                return stat_eval
    else:
        return stat_eval

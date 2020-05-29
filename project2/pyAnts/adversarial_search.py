
def minimax(node, depth, maximizing_player, a, b, ab_switch, in_danger, en_masse):
    # What makes a node Terminal?
    if depth == 0 or node.is_terminal():
        return node.state_evaluation(in_danger, en_masse)

    if maximizing_player:
        value = -100000

        for child in node.successor_states():
            value = max(value, minimax(child, depth-1, False, a, b, ab_switch, in_danger, en_masse))
            a = max(value, a)
            if a >= b and ab_switch:
                break 

        return value
    
    else:
        value = +100000

        for child in node.successor_states():
            value = min(value, minimax(child, depth-1, True, a, b, ab_switch, in_danger, en_masse))
            b = min(b, value)
            if a >= b and ab_switch:
                break
        
        return value


def minimax(node, depth, maximizingPlayer, a, b, abswitch):
    # What makes a node Terminal?
    if depth == 0 or node.is_terminal():
        return node.state_evaluation()

    if maximizingPlayer:
        value = -100000

        for child in node.successor_states():
            value = max(value, minimax(child, depth-1, False, a, b, abswitch))
            a = max(value, a)
            if a >= b and abswitch:
                break 

        return value
    
    else:
        value = +100000

        for child in node.successor_states():
            value = min(value, minimax(child, depth-1, True, a, b, abswitch))
            b = min(b, value)
            if a >= b and abswitch:
                break 
        
        return value



#Issue No.1 : When is a node a terminal node? 
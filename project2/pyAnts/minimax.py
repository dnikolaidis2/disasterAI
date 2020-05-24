
def minimax(node, depth, maximizingPlayer, a, b):
    if depth == 0 or node.is_terminal():     #What makes a node Terminal? 
        return node.state_evaluation()

    if maximizingPlayer:
        value = -100000

        for child in node.successor_states():
            value = max(value, minimax(child, depth-1, False, a, b))
            a = max(value, a)
            if a >= b:
                break 

        return value
    
    else:
        value = +100000

        for child in node.successor_states():
            value = min(value, minimax(child, depth-1, True, a, b))
            b = min(b, value)
            if a >= b: 
                break 
        
        return value



#Issue No.1 : When is a node a terminal node? 
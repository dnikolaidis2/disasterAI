from pyAnts.board import PositionStruct
from pyAnts.move import MoveStruct
from argparse import ArgumentParser
from pyAnts.comm import connectToTarget, recvMsg, NM_COLOR_B,\
    NM_COLOR_W, NM_NEW_POSITION, NM_QUIT, NM_REQUEST_MOVE,\
    NM_REQUEST_NAME, sendName, getPosition, sendMove
from pyAnts.globals import BLACK, WHITE, DEFAULT_PORT, MinimaxStats
from os import close
from pyAnts.adversarial_search import minimax
from copy import copy
from time import time
from statistics import mean

gamePosition = None                 # Position we are going to use

myMove = MoveStruct()               # move to save our choice and send it to the server

myColor = -1                        # to store our color
mySocket = 0                        # our socket

agentName = "AgeAnt"                # agent name

ip = "127.0.0.1"                    # default ip


if __name__ == "__main__":
    parser = ArgumentParser(description='This is the python version of the client program for the Project TUCAnts')
    parser.add_argument('-i', metavar='ip', default="127.0.0.1", help="The ip to connect to.")
    parser.add_argument('-p', metavar='port', default=DEFAULT_PORT, help="The port to connect to.")
    parser.add_argument('-name', default="AgeAnt", help="Give the agent a new name.")
    parser.add_argument('-depth', default=6, help="Depth from minimax algorithm.", type=int)
    parser.add_argument('-nalphabeta', default=True, action='store_false', help="Disable alpha beta pruning algorithm.")
    parser.add_argument('-qsearch', default=False, action='store_true',
                        help="Enable quiescence search in minimax algorithm.")
    parser.add_argument('-nindanger', default=True, action='store_false', help="Disables in_danger evaluation part.")
    parser.add_argument('-nenamsse', default=True, action='store_false', help="Disables en_masse evaluation part.")
    parser.add_argument('-minimaxstats', default=False, action='store_true',
                        help="Enables statistics gathering in minimax")
    parser.add_argument('-perf', default=False, action='store_true',
                        help="Enables performance measurements for minimax")

    args = parser.parse_args()
    MinimaxStats.enabled = args.minimaxstats
    agentName = args.name

    ip = args.i

    mySocket = connectToTarget(args.p, ip, mySocket)

    while True:
        msg = recvMsg(mySocket)

        if gamePosition is None:
            gamePosition = PositionStruct()

        if msg == NM_REQUEST_NAME:                # server asks for our name
            sendName(agentName, mySocket)
        elif msg == NM_NEW_POSITION:              # server is trying to send us a new position
            getPosition(gamePosition, mySocket)
            print(gamePosition)
            gamePosition.update_enemy_statistics()        # Update statistics based on enemy move
            if gamePosition.is_terminal():
                gamePosition = None

        elif msg == NM_COLOR_W:                   # server informs us that we have WHITE color
            myColor = WHITE
            gamePosition.set_color(myColor)
            print(f"My color is {myColor}")

        elif msg == NM_COLOR_B:                   # server informs us that we have BLACK color
            myColor = BLACK
            gamePosition.set_color(myColor)
            print(f"My color is {myColor}")
        
        elif msg == NM_REQUEST_MOVE:		# server requests our move
            gamePosition.set_color(myColor)
            myMove.color = myColor 
            if not gamePosition.can_move(myColor):
                tmpPos = copy(gamePosition)
                tmpPos.set_color(tmpPos.enemy_color)

                final_round = False
                for state in tmpPos.successor_states():
                    if state.is_terminal():
                        final_round = True
                    else:
                        final_round = False
                        break

                if final_round:
                    gamePosition = None

                myMove.tile[0][0] = -1		# null move
                sendMove(myMove, mySocket)  # send our move
                continue
            else:
                if args.perf:
                    start = time()

                max_value = -1000000
                selected_node = None
                for node in gamePosition.successor_states():
                    if MinimaxStats.enabled:
                        MinimaxStats.expansion_count[str(args.depth)] += 1

                    value = minimax(node, args.depth, True, -100000, 100000,
                                    args.nalphabeta, args.nqsearch, args.nindanger, args.nenamsse)
                    if value > max_value:
                        max_value = value
                        selected_node = node

                gamePosition = selected_node
                if selected_node.is_terminal():
                    gamePosition = None
                sendMove(selected_node.move, mySocket)			# send our move

                if args.perf:
                    end = time()
                    MinimaxStats.perf_times.append(end - start)

        elif msg == NM_QUIT:			# server wants us to quit...we shall obey
            if args.perf:
                if len(MinimaxStats.perf_times) > 0:
                    print(f"Average decision time(Only minimax): {mean(MinimaxStats.perf_times):.3f}s")

            if MinimaxStats.enabled:
                for i in MinimaxStats.expansion_count:
                    print(f"|{i:^14s}", end='')
                print(f"|{'Total':^14s}|")

                for i in MinimaxStats.expansion_count.values():
                    print(f"|{i:^14d}", end='')
                print(f"|{sum(MinimaxStats.expansion_count.values()):^14d}|")

            close(mySocket)
            exit(0)

        else:
            print("Wrong Signal!")
            exit(0)


"""
# *****************************************************
                    # random player - not the most efficient implementation
    
                    if myColor == WHITE:		# find movement's direction
                        playerDirection = 1
                    else:
                        playerDirection = -1
    
                    jumpPossible = False    # determine if we have a jump available
                    for i in range(BOARD_ROWS):
                        for j in range(BOARD_COLUMNS):
                            if gamePosition.board[i][j] == myColor:
                                if gamePosition.can_jump(i, j, myColor):
                                    jumpPossible = True
    
                    while True:
                        i = randint(0, BOARD_ROWS - 1)
                        j = randint(0, BOARD_COLUMNS - 1)
    
                        if gamePosition.board[i][j] == myColor:		# find a piece of ours
                            myMove.tile[0][0] = i		        # piece we are going to move
                            myMove.tile[1][0] = j
                            if jumpPossible is False:
                                myMove.tile[0][1] = i + 1 * playerDirection
                                myMove.tile[0][2] = -1
                                if random() <= 0.5:	            # with 50% chance try left and then right
                                    myMove.tile[1][1] = j - 1
                                    if gamePosition.is_legal(myMove):
                                        break
    
                                    myMove.tile[1][1] = j + 1
                                    if gamePosition.is_legal(myMove):
                                        break
                                else:	        # the other 50%...try right first and then left
                                    myMove.tile[1][1] = j + 1
                                    if gamePosition.is_legal(myMove):
                                        break
    
                                    myMove.tile[1][1] = j - 1
                                    if gamePosition.is_legal(myMove):
                                        break
                            else:       # jump possible
                                if gamePosition.can_jump(i, j, myColor):
                                    k = 1
                                    while gamePosition.can_jump(i, j, myColor) != 0:
                                        myMove.tile[0][k] = i + 2 * playerDirection
                                        if random() <= 0.5:     # 50% chance
                                            if gamePosition.can_jump(i, j, myColor) % 2 == 1:		# left jump possible
                                                myMove.tile[1][k] = j - 2
                                            else:
                                                myMove.tile[1][k] = j + 2
                                        else:       # 50%
                                            if gamePosition.can_jump(i, j, myColor) > 1:		# right jump possible
                                                myMove.tile[1][k] = j + 2
                                            else:
                                                myMove.tile[1][k] = j - 2
    
                                        if k + 1 == MAXIMUM_MOVE_SIZE:      # maximum tiles reached
                                            break
    
                                        myMove.tile[0][k + 1] = -1		# maximum tiles not reached
    
                                        i = myMove.tile[0][k]   # we will try to jump from this point in the next loop
                                        j = myMove.tile[1][k]
    
                                        k += 1
                                    break
                    # end of random
                    # *****************************************************
"""

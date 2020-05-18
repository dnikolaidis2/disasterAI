from pyAnts.board import PositionStruct, doMove, canMove, isLegal, canJump
from pyAnts.move import MoveStruct
from argparse import ArgumentParser
from pyAnts.comm import connectToTarget, recvMsg, NM_COLOR_B,\
    NM_COLOR_W, NM_NEW_POSITION, NM_PREPARE_TO_RECEIVE_MOVE,\
    NM_QUIT, NM_REQUEST_MOVE, NM_REQUEST_NAME, sendName, getPosition,\
    getMove, sendMove
from pyAnts.globals import BLACK, WHITE, getOtherSide, BOARD_COLUMNS, BOARD_ROWS, MAXIMUM_MOVE_SIZE, DEFAULT_PORT
from os import close
from random import random, randint

gamePosition = PositionStruct()     # Position we are going to use

moveReceived = MoveStruct()         # temporary move to retrieve opponent's choice
myMove = MoveStruct()               # move to save our choice and send it to the server

myColor = -1                        # to store our color
mySocket = 0                        # our socket

agentName = "Python agent!"         # agent name

ip = "127.0.0.1"                    # default ip


if __name__ == "__main__":
    parser = ArgumentParser(description='This is the python version of the client program for the Project TUCAnts')
    parser.add_argument('-i', metavar='ip', default="127.0.0.1", help="The ip to connect to.")
    parser.add_argument('-p', metavar='port', default=DEFAULT_PORT, help="The port to connect to.")

    args = parser.parse_args()

    ip = args.i

    mySocket = connectToTarget(args.p, ip, mySocket)

    while True:
        msg = recvMsg(mySocket)

        if msg == NM_REQUEST_NAME:                # server asks for our name
            sendName(agentName, mySocket)
        elif msg == NM_NEW_POSITION:              # server is trying to send us a new position
            getPosition(gamePosition, mySocket)
            print(gamePosition)
        elif msg == NM_COLOR_W:                   # server informs us that we have WHITE color
            myColor = WHITE
            print(f"My color is {myColor}",)

        elif msg == NM_COLOR_B:                   # server informs us that we have BLACK color
            myColor = BLACK
            print(f"My color is {myColor}")

        elif msg == NM_PREPARE_TO_RECEIVE_MOVE:     # server informs us that he will send opponent's move
            getMove(moveReceived, mySocket)
            moveReceived.color = getOtherSide(myColor)
            doMove(gamePosition, moveReceived)		# play opponent's move on our position
            print(gamePosition)

        elif msg == NM_REQUEST_MOVE:		# server requests our move
            myMove.color = myColor
            if not canMove(gamePosition, myColor):
                myMove.tile[0][0] = -1		# null move
            else:
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
                            if canJump(i, j, myColor, gamePosition):
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
                                if isLegal(gamePosition, myMove):
                                    break

                                myMove.tile[1][1] = j + 1
                                if isLegal(gamePosition, myMove):
                                    break
                            else:	        # the other 50%...try right first and then left
                                myMove.tile[1][1] = j + 1
                                if isLegal(gamePosition, myMove):
                                    break

                                myMove.tile[1][1] = j - 1
                                if isLegal(gamePosition, myMove):
                                    break
                        else:       # jump possible
                            if canJump(i, j, myColor, gamePosition):
                                k = 1
                                while canJump(i, j, myColor, gamePosition) != 0:
                                    myMove.tile[0][k] = i + 2 * playerDirection
                                    if random() <= 0.5:     # 50% chance
                                        if canJump(i, j, myColor, gamePosition) % 2 == 1:		# left jump possible
                                            myMove.tile[1][k] = j - 2
                                        else:
                                            myMove.tile[1][k] = j + 2
                                    else:       # 50%
                                        if canJump(i, j, myColor, gamePosition) > 1:		# right jump possible
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

            sendMove(myMove, mySocket)			# send our move
            # printf("i chose to go from (%d,%d), to (%d,%d)\n",myMove.tile[0][0],myMove.tile[1][0],myMove.tile[0][1],myMove.tile[1][1]);
            doMove(gamePosition, myMove)		# play our move on our position
            print(gamePosition)

        elif msg == NM_QUIT:			# server wants us to quit...we shall obey
            close(mySocket)
            exit()

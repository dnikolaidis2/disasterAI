MAXIMUM_MOVE_SIZE = 6

# The size of our board
BOARD_COLUMNS = 8
BOARD_ROWS = 12
BOARD_SIZE = 8

# Values for each possible tile state
WHITE = 0
BLACK = 1
EMPTY = 2
RTILE = 3
ILLEGAL = 4

# max size of our name
MAX_NAME_LENGTH = 16

# default port for client and server
DEFAULT_PORT = "6001"


def getOtherSide(side):
    return 1 - side

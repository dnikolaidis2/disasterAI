from ctypes import CDLL, c_byte, Structure, pointer
from .globals import BOARD_ROWS, BOARD_COLUMNS
from os import environ

if "LD_LIBRARY_PATH" not in environ:
	raise ImportError("LD_LIBRARY_PATH must be set to the location of libboard.so before running!")

board_lib = CDLL('libboard.so')


# Position struct to store board, score and player's turn
class PositionStruct(Structure):
	_fields_ = [("board", (c_byte * BOARD_COLUMNS) * BOARD_ROWS),
				("score", (c_byte * 2)),
				("turn", c_byte)]


def initPosition(pos):
	"""
	Initializes position
	:param pos:
	:return:
	"""
	board_lib.initPosition(pointer(pos))


def printBoard(board):
	"""
	Prints board
	:param board:
	:return:
	"""
	board_lib.printBoard(board)


def printPosition(pos):
	"""
	Prints board along with Player's turn and score
	:param pos:
	:return:
	"""
	board_lib.printPosition(pointer(pos))


def doMove(pos, moveToDO):
	"""
	Plays moveToDo on position pos
	Caution!!! does not check if it is legal! Simply does the move!
	:param pos:
	:param moveToDO:
	:return:
	"""
	board_lib.doMove(pointer(pos), pointer(moveToDO))


def canJump(row, col, player, pos):
	"""
	Returns 1 if we can jump to the left 2 if we can jump to the right 3 if we can jump
	both directions and 0 if no jump is possible row,col can be empty. So it can also be
	used to determine if we can make a jump from a position we do not occupy.
	Caution!!! does no checks if we are inside the board
	:param row:
	:param col:
	:param player:
	:param pos:
	:return:
	"""
	return board_lib.canJump(c_byte(row), c_byte(col), c_byte(player), pointer(pos))


def canJumpTo(row, col, player, pos, rowDest, colDest):
	"""
	Like canJump() it doesn't need row, col to be occupied by a piece.
	Caution!!! does no checks if we are inside board
	:param row:
	:param col:
	:param player:
	:param pos:
	:param rowDest:
	:param colDest:
	:return:
	"""
	return bool(board_lib.canJumpTo(c_byte(row), c_byte(col), c_byte(player),
									pointer(pos), c_byte(rowDest), c_byte(colDest)))


def canMove(pos, player):
	"""
	Determines if player can move
	:param pos:
	:param player:
	:return:
	"""
	return bool(board_lib.canMove(pointer(pos), c_byte(player)))


def isLegal(pos, moveToCheck):
	"""
	Determines if a move is legal
	:param pos:
	:param moveToCheck:
	:return:
	"""
	return bool(board_lib.isLegal(pointer(pos), pointer(moveToCheck)))


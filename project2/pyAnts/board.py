from ctypes import CDLL, c_byte, Structure, pointer
from .globals import BOARD_ROWS, BOARD_COLUMNS, WHITE, BLACK, EMPTY, ILLEGAL, RTILE
from os import environ

if "LD_LIBRARY_PATH" not in environ:
	raise ImportError("LD_LIBRARY_PATH must be set to the location of libboard.so before running!")

board_lib = CDLL('libboard.so')


# Position struct to store board, score and player's turn
class PositionStruct(Structure):
	_fields_ = [("board", (c_byte * BOARD_COLUMNS) * BOARD_ROWS),
				("score", (c_byte * 2)),
				("turn", c_byte)]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		initPosition(self)

	def __repr__(self):
		return positionToString(self)

	def __hash__(self):
		return hash(self.__repr__())

	def __eq__(self, other):
		if isinstance(other, PositionStruct):
			return self.__hash__() == other.__hash__()
		else:
			return False

	def can_jump(self, row, col, player):
		return canJump(row, col, player, self)

	def can_jump_to(self, row, col, player, row_dest, col_dest):
		return canJumpTo(row, col, player, self, row_dest, col_dest)

	def do_move(self, move):
		if self.is_legal(move):
			doMove(self, move)
			return True
		else:
			return False

	def is_legal(self, move):
		return isLegal(self, move)

	def can_move(self, player):
		return canMove(self, player)


def initPosition(pos):
	"""
	Initializes position
	:param pos:
	:return:
	"""
	board_lib.initPosition(pointer(pos))


def boardToString(board):
	# Print the upper section
	out = "    "
	for i in range(BOARD_COLUMNS):
		out += f"{i} "
	out += "\n  +"
	for i in range(2 * BOARD_COLUMNS + 1):
		out += "-"
	out += "+\n"

	# Print board
	for i in range(BOARD_ROWS):
		if i >= 10:
			out += f"{i}| "
		else:
			out += f"0{i}| "
		for j in range(BOARD_COLUMNS):
			if board[i][j] == WHITE:
				out += "W "
			elif board[i][j] == BLACK:
				out += "B "
			elif board[i][j] == EMPTY:
				out += ". "
			elif board[i][j] == ILLEGAL:
				out += "# "
			elif board[i][j] == RTILE:
				out += "* "
			else:
				print("ERROR: Unknown character in board (boardToString)")
				exit(1)
		if i >= 10:
			out += f"|{i} \n"
		else:
			out += f"|0{i} \n"

	# Print the lower section
	out += "  +"
	for i in range(2 * BOARD_COLUMNS + 1):
		out += "-"
	out += "+\n"
	out += "    "
	for i in range(BOARD_COLUMNS):
		out += f"{i} "
	out += "\n"
	return out


def positionToString(pos):
	# board
	out = boardToString(pos.board)

	# turn
	if pos.turn == WHITE:
		out += "Turn: WHITE"
	elif pos.turn == BLACK:
		out += "Turn: BLACK"
	else:
		out += "Turn: -"

	out += "\n"

	# score
	out += f"Score is  W: {pos.score[WHITE]}  B: {pos.score[BLACK]}\n"
	return out


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


from ctypes import CDLL, c_byte, Structure, pointer
from .globals import BOARD_ROWS, BOARD_COLUMNS, WHITE, BLACK, EMPTY, ILLEGAL, RTILE, MAXIMUM_MOVE_SIZE
from .move import MoveStruct, MoveType
from os import environ
from collections import deque
from copy import copy

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

		if "init" in kwargs and kwargs["init"]:
			initPosition(self)

		self.pieces = 12
		self.queens = 0
		self.gath_food = 0
		self.enemy_pieces = 12
		self.enemy_queens = 0
		self.enemy_gath_food = 0
		self.available_food = -1
		self.evaluation = 0
					


		if "empty" in kwargs and kwargs["empty"]:
			for i in range(BOARD_ROWS):
				for j in range(BOARD_COLUMNS):
					self.board[i][j] = EMPTY

		if "parent" in kwargs:
			self.parent = kwargs["parent"]
		else:
			self.parent = None

		if "move" in kwargs:
			self.move = kwargs["move"]
		else:
			self.move = None

		if "turn" in kwargs:
			self.turn = kwargs["turn"]

		self.direction = 1
		self.color = 0		#Default Color
		self.enemy_color = 1
		self.set_direction()

	def __repr__(self):
		return positionToString(self)

	def __hash__(self):
		return hash(self.__repr__())

	def __eq__(self, other):
		if isinstance(other, PositionStruct):
			return self.__hash__() == other.__hash__()
		else:
			return False

	def __bool__(self):
		return self.can_move(self.turn)

	def get_available_moves(self):
		moves = deque()
		jump_moves = 0
		queen_moves = 0
		food_moves = 0

		for i in range(BOARD_ROWS):
			for j in range(BOARD_COLUMNS):
				if self.board[i][j] == self.turn:
					jumps = self.get_all_jumps(i, j)
					jumps_len = len(jumps)
					jumps += [moves.pop() for i in range(jump_moves)]
					jumps.sort(key=(lambda x: x.jump_count), reverse=True)
					moves.extendleft(jumps)
					jump_moves += jumps_len
					queen_moves += jumps_len
					food_moves += jumps_len

					i_tmp = i + self.direction
					if i_tmp < BOARD_ROWS:
						j_tmp = j + 1
						if j_tmp < BOARD_COLUMNS:
							if self.board[i_tmp][j_tmp] == EMPTY or \
								self.board[i_tmp][j_tmp] == RTILE:
								if self.board[i_tmp][j_tmp] == RTILE:
									move_type = MoveType.FOOD
									moves.insert(food_moves, MoveStruct(type=move_type, color=self.turn,
																		init_pos=[i, j], dest_pos=[i_tmp, j_tmp]))
									food_moves += 1
								elif i_tmp == 0 or i_tmp == 11:
									move_type = MoveType.QUEEN
									moves.insert(queen_moves, MoveStruct(type=move_type, color=self.turn,
																		init_pos=[i, j], dest_pos=[i_tmp, j_tmp]))
									queen_moves += 1
									food_moves += 1
								else:
									move_type = MoveType.MOVE
									moves.append(MoveStruct(type=move_type, color=self.turn,
															init_pos=[i, j], dest_pos=[i_tmp, j_tmp]))

						j_tmp = j - 1
						if j_tmp >= 0:
							if self.board[i_tmp][j_tmp] == EMPTY or \
									self.board[i_tmp][j_tmp] == RTILE:
								if self.board[i_tmp][j_tmp] == RTILE:
									move_type = MoveType.FOOD
									moves.insert(food_moves, MoveStruct(type=move_type, color=self.turn,
																		init_pos=[i, j], dest_pos=[i_tmp, j_tmp]))
									food_moves += 1
								elif i_tmp == 0 or i_tmp == 11:
									move_type = MoveType.QUEEN
									moves.insert(queen_moves, MoveStruct(type=move_type, color=self.turn,
																		init_pos=[i, j], dest_pos=[i_tmp, j_tmp]))
									queen_moves += 1
									food_moves += 1
								else:
									move_type = MoveType.MOVE
									moves.append(MoveStruct(type=move_type, color=self.turn,
															init_pos=[i, j], dest_pos=[i_tmp, j_tmp]))

		return moves

	def can_jump(self, row, col, player):
		return canJump(row, col, player, self)

	def can_jump_to(self, row, col, player, row_dest, col_dest):
		return canJumpTo(row, col, player, self, row_dest, col_dest)

	def do_move(self, move):
		if self.is_legal(move):
			doMove(self, move)
			self.move = move
			return True
		else:
			return False

	def is_legal(self, move):
		return isLegal(self, move)

	def can_move(self, player):
		return canMove(self, player)

	def get_all_jumps(self, row, col, jump_to_here=None):
		ret = []
		jump = self.can_jump(row, col, self.turn)
		if jump != 0:
			if jump_to_here:
				k = jump_to_here.jump_count + 1
				new_move = jump_to_here
				new_move.jump_count = k
			else:
				k = 1
				new_move = MoveStruct(type=MoveType.JUMP, color=self.turn, jump_count=k, init_pos=[row, col])

			if k + 1 > MAXIMUM_MOVE_SIZE:
				if jump_to_here:
					ret.append(jump_to_here)

				return ret
			elif k + 1 != MAXIMUM_MOVE_SIZE:
				new_move.tile[0][k + 1] = -1

			new_move.tile[0][k] = row + (2 * self.direction)
			if jump == 1:
				new_move.tile[1][k] = col - 2
				ret += self.get_all_jumps(new_move.tile[0][k], new_move.tile[1][k], new_move)
			elif jump == 2:
				new_move.tile[1][k] = col + 2
				ret += self.get_all_jumps(new_move.tile[0][k], new_move.tile[1][k], new_move)
			elif jump == 3:
				r_new_move = copy(new_move)
				new_move.tile[1][k] = col - 2
				r_new_move.tile[1][k] = col + 2
				ret += self.get_all_jumps(new_move.tile[0][k], new_move.tile[1][k], new_move)
				ret += self.get_all_jumps(r_new_move.tile[0][k], r_new_move.tile[1][k], r_new_move)
		else:
			if jump_to_here:
				ret.append(jump_to_here)

		return ret

	def successor_states(self):
		moves = self.get_available_moves()
		child_states = []
		for move in moves:
			#Create copied child state to apply Moves.
			child_states.append(copy(self))
			child_states[-1].parent = self
			if not child_states[-1].do_move(move):
				continue 
			
			#Update statistics for child
			child_states[-1].move = move	#Is this necessary? 
			child_states[-1].update_statistics() 			 
			child_states[-1].print_statistics()
			
			#Then give an evaluation for each state.
			child_states[-1].evaluation = child_states[-1].state_evaluation()
			print('\nState evaluation : '+str(child_states[-1].evaluation))
	 
			#For now we expect the first move to always be the best move for testing.. 
		return child_states
		

	def set_turn(self, turn):
		self.turn = turn
		self.set_direction()

	def set_direction(self, direction=None):
		if direction:
			self.direction = direction
		else:
			if self.turn == BLACK:
				self.direction = -1
			else:
				self.direction = 1

	def state_evaluation(self):
		
		return self.pieces + self.gath_food + self.queens - self.enemy_pieces - self.enemy_gath_food - self.enemy_queens    

	# Update statistics after agent's turn
	def update_statistics(self):		
		self.pieces = get_available_pieces(self, self.color)
		if self.parent is not None:
			self.get_available_food()
			if self.available_food < self.parent.available_food:
				self.gath_food += 1
		
			if self.pieces < self.parent.pieces:
				self.queens += 1

		self.enemy_pieces -= self.move.jump_count
 

	# Update statistics after enemy's turn
	def update_enemy_statistics(self):
		if self.available_food >= 0:
			prev_food = copy(self.available_food)
			self.get_available_food()
			if self.available_food < prev_food:				
				self.enemy_gath_food += 1
		else:
			self.get_available_food()
		updated_enemy_pieces = get_available_pieces(self, self.enemy_color)
		if updated_enemy_pieces < self.enemy_pieces:
			self.enemy_queens += (self.enemy_pieces - updated_enemy_pieces)
			self.enemy_pieces = updated_enemy_pieces  
		
	def get_available_food(self):
		self.available_food = 0
		for i in range(BOARD_ROWS):
			for j in range(BOARD_COLUMNS):
				if self.board[i][j] == RTILE:
					self.available_food += 1 
		

	def print_statistics(self):
		print('\n\nMy Pieces :'+str(self.pieces))
		print('My Food :'+str(self.gath_food))
		print('My Queens :'+str(self.queens))
		print('Enemy Pieces :'+str(self.enemy_pieces))
		print('Enemy Food :'+str(self.enemy_gath_food))
		print('Enemy Queens :'+str(self.enemy_queens))
		print('Total Food :'+str(self.available_food))

	def set_color(self, color):
		self.color = color 
		self.enemy_color = int(not color)

	def is_terminal(self):
		for i in range(BOARD_ROWS):
			for j in range(BOARD_COLUMNS):
				if self.board != EMPTY:
					return 0
		return 1

def get_available_pieces(pos, color):
	pieces = 0
	for i in range(BOARD_ROWS):
		for j in range(BOARD_COLUMNS):
			if pos.board[i][j] == color:
				pieces += 1
	return pieces




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


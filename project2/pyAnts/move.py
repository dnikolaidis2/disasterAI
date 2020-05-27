from ctypes import Structure, c_byte
from .globals import MAXIMUM_MOVE_SIZE, WHITE, BLACK
from enum import Enum


class MoveType(Enum):
	JUMP = 0
	QUEEN = 1
	FOOD = 2
	MOVE = 3


# Struct to store Move and color of the player
class MoveStruct(Structure):
	_fields_ = [("tile", (c_byte*MAXIMUM_MOVE_SIZE)*2),
				("color", c_byte)]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		if "type" in kwargs:
			self.type = kwargs["type"]
		else:
			self.type = None

		if "color" in kwargs:
			self.color = kwargs["color"]

		if self.type == MoveType.JUMP and "jump_count" in kwargs:
			self.jump_count = kwargs["jump_count"]
		else:
			self.jump_count = 0

		if "init_pos" in kwargs:
			self.tile[0][0] = kwargs["init_pos"][0]
			self.tile[1][0] = kwargs["init_pos"][1]

		if "dest_pos" in kwargs:
			self.tile[0][1] = kwargs["dest_pos"][0]
			self.tile[1][1] = kwargs["dest_pos"][1]
			self.tile[0][2] = -1

	def __repr__(self):
		out = ""
		if self.color == WHITE:
			out += "Move: WHITE"
		elif self.color == BLACK:
			out += "Move: BLACK"
		else:
			out += "Move: -"

		for i in range(MAXIMUM_MOVE_SIZE):
			if self.tile[0][i] == -1:
				break
			else:
				out += '\n'

			out += f"{i}| {self.tile[0][i]:2}, {self.tile[1][i]:2}"
		return out

	def __hash__(self):
		return hash(self.__repr__())

	def __eq__(self, other):
		if isinstance(other, MoveStruct):
			return self.__hash__() == other.__hash__()
		else:
			return False

	def get_destination(self):
		if self.tile[0][0] == -1:
			return None

		for i in reversed(range(MAXIMUM_MOVE_SIZE)):
			if self.tile[0][i] == -1:
				return [self.tile[0][i - 1], self.tile[1][i - 1]]

		return [self.tile[0][MAXIMUM_MOVE_SIZE], self.tile[1][MAXIMUM_MOVE_SIZE]]


"""
Caution!

tile[0][0] and tile[1][0] holds the row and col of the piece we want to move!
All the other coordinates are the tiles that this piece will go to.

for a move to be valid the tile[0][i+1] (where tile[0][i] holds the row of the last tile of our move) must be -1.
Only exception to this is when we have to make the maximum number of moves.


A Null move (the only legal move when we cannot move) has tile[0][0] = -1.

Server can ask for a move even we have none available.

"""

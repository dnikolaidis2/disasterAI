from ctypes import Structure, c_byte
from .globals import MAXIMUM_MOVE_SIZE, WHITE, BLACK


# Struct to store Move and color of the player
class MoveStruct(Structure):
	_fields_ = [("tile", (c_byte*MAXIMUM_MOVE_SIZE)*2),
				("color", c_byte)]

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


"""
Caution!

tile[0][0] and tile[1][0] holds the row and col of the piece we want to move!
All the other coordinates are the tiles that this piece will go to.

for a move to be valid the tile[0][i+1] (where tile[0][i] holds the row of the last tile of our move) must be -1.
Only exception to this is when we have to make the maximum number of moves.


A Null move (the only legal move when we cannot move) has tile[0][0] = -1.

Server can ask for a move even we have none available.

"""

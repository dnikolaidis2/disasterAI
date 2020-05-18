from ctypes import Structure, c_byte
from .globals import MAXIMUM_MOVE_SIZE


# Struct to store Move and color of the player
class MoveStruct(Structure):
	_fields_ = [("tile", (c_byte*MAXIMUM_MOVE_SIZE)*2),
				("color", c_byte)]


"""
Caution!

tile[0][0] and tile[1][0] holds the row and col of the piece we want to move!
All the other coordinates are the tiles that this piece will go to.

for a move to be valid the tile[0][i+1] (where tile[0][i] holds the row of the last tile of our move) must be -1.
Only exception to this is when we have to make the maximum number of moves.


A Null move (the only legal move when we cannot move) has tile[0][0] = -1.

Server can ask for a move even we have none available.

"""

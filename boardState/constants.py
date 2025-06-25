from enum import Enum


EMPTY_CELL_BLOCK_IND  = 0
# actually, I don't use it for now.
# It's equal to 1, because in ansi colors decimal codes that end with 1 represent red color
HIGHLIGHTED_BLOCK_IND = 1
# WARNING: should be an integer
# actually it's just a side length of one block tile
SCALE_FACTOR = 1

BLOCK_DSNT_FIT_ERR_MSG = "Error: block doesn't fit on the board"
class BlockTraverseDir(Enum):
    DIRECTION_DOWN  = (1, 0)
    DIRECTION_RIGHT = (0, 1)

from enum import Enum


EMPTY_CELL_BLOCK_IND   = 0
# actually, I don't use it for now.
# It's equal to 1, because in ansi colors decimal codes that end with 1 represent red color
HIGHLIGHTED_BLOCK_IND  = 1
MAX_BOARD_SCALE_FACTOR = 4
MAX_BOARD_WIDTH        = 8
MAX_BOARD_HEIGHT       = 8
MAX_NUMBER_OF_BLOCKS   = 15 # I have limited amount of ANSI colors (only 16 and black is for empty cells)
MIN_BLOCK_SIDE_LEN     = 2
HIGHLIGHTED_BLOCK_CHAR = '.'


class BlockTraverseDir(Enum):
    DIRECTION_DOWN  = (1, 0)
    DIRECTION_RIGHT = (0, 1)

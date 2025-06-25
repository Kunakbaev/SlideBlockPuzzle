
from enum import StrEnum

class Block:
    def __init__(self, rowPos, colPos, isHorizontal, sideLen, blockInd):
        self.rowPos       = rowPos
        self.colPos       = colPos
        self.isHorizontal = isHorizontal
        self.sideLen      = sideLen
        self.blockInd     = blockInd

class BlockDirs(StrEnum):
    HORIZONTAL = "h"
    VERTICAL   = "v"

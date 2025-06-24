
from enum import StrEnum

class Block:
    def __init__(self, rowPos, colPos, isHorizontal, sideLen):
        self.rowPos       = rowPos
        self.colPos       = colPos
        self.isHorizontal = isHorizontal
        self.sideLen      = sideLen

class BlockDirs(StrEnum):
    HORIZONTAL = "h"
    VERTICAL   = "v"

import sys
from enum import Enum
from terminalScreen import TerminalBgStyles, getBlockColorStyle, moveCursorToPos
from boardState.constants import *

class BoardState:
    def __init__(self, width, height, escGatePerimeterInd, goalBlockInd):
        self.width               = width
        self.height              = height
        self.board               = [[EMPTY_CELL_BLOCK_IND for j in range(width)] for i in range(height)]
        self.numberOfBlocks      = 0 # counts how many are already on the board
        self.escGatePerimeterInd = escGatePerimeterInd
        self.goalBlockInd        = goalBlockInd

    # adds block with one side len equal to one and other equal to passed parameter
    # (rowPos, colPos) - position of top left corner of rectangle
    def addBlock(self, block) -> None:
        print(BlockTraverseDir.DIRECTION_DOWN.value)
        dx, dy = BlockTraverseDir.DIRECTION_DOWN.value
        if block.isHorizontal:
            dx, dy = BlockTraverseDir.DIRECTION_RIGHT.value

        self.numberOfBlocks += 1
        rowPos = block.rowPos
        colPos = block.colPos
        for _ in range(block.sideLen):
            if min(rowPos, colPos) < 0 or \
               rowPos >= self.height   or \
               colPos >= self.width: # check if cell position is valid
                print(BLOCK_DSNT_FIT_ERR_MSG)
                assert False

            self.board[rowPos][colPos] = self.numberOfBlocks
            rowPos += dy
            colPos += dx

    def isFinalState(self, gatePerimeterInd, goalBlockInd) -> bool:
        pass

    def getBgStyleForCell(self, rowInd, colInd):
        # cell is inside board and not on the edge
        if 1 <= min(rowInd, colInd) and \
           rowInd <= self.height    and \
           colInd <= self.width:
            blockInd = int(self.board[rowInd - 1][colInd - 1])
            # print(rowInd, colInd, blockInd)
            blockColorStyle = getBlockColorStyle(blockInd)
            return blockColorStyle

        # otherwise, cell is located on the perimeter of the board
        perimeterCellInd = rowInd + colInd
        if rowInd == self.height + 1 or \
          (colInd == 0 and rowInd != 0):
            perimeterCellInd = (self.width + self.height + 2) * 2 - perimeterCellInd

        blockColorStyle = TerminalBgStyles.BORDER
        if perimeterCellInd == self.escGatePerimeterInd:
            blockColorStyle = TerminalBgStyles.ESC_GATE
        return blockColorStyle

    def updateCellAndRedrawIt(self, rowInd, colInd, newBlockInd):
        self.board[rowInd][colInd] = newBlockInd
        blockColorStyle = self.getBgStyleForCell(rowInd + 1, colInd + 1)
        for i in range(SCALE_FACTOR):
            for j in range(SCALE_FACTOR):
                row = SCALE_FACTOR * (rowInd + 1) + 1 + i
                col = SCALE_FACTOR * (colInd + 1) * 2 + j * 2
                moveCursorToPos(row + 1, col + 1)
                print(blockColorStyle * 2, end="")
        sys.stdout.flush()

    def displayBoardState(self):
        print("Board state:")
        # +2 because of edge tiles
        # each tile is scaled, so it's side is equal to SCALE_FACTOR
        for i in range((self.height + 2) * SCALE_FACTOR):
            rowInd = i // SCALE_FACTOR
            for j in range((self.width + 2) * SCALE_FACTOR):
                colInd = j // SCALE_FACTOR

                blockColorStyle = self.getBgStyleForCell(rowInd, colInd)
                # line height is approximately 2 * one symbol width, so to consecutive chars for a nice square
                print(blockColorStyle * 2, end='')
            print()
        print()

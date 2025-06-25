import sys
from enum import Enum

from terminalScreen import TerminalBgStyles, getBlockColorStyle, moveCursorToPos
from boardState.constants import *
from hashlib import sha256
from json import dumps


def getNumberSign(num):
    if num < 0:
        return -1
    return num > 0


def getDirectionBy2Cells(
    row1, col1,
    row2, col2
):
    deltaRow = getNumberSign(row2 - row1)
    deltaCol = getNumberSign(col2 - col1)
    return deltaRow, deltaCol


class BoardState:
    def __init__(self, width, height, escGatePerimeterInd, goalBlockInd):
        self.width               = width
        self.height              = height
        self.board               = [[EMPTY_CELL_BLOCK_IND for j in range(width)] for i in range(height)]
        self.numberOfBlocks      = 0 # counts how many are already on the board
        self.escGatePerimeterInd = escGatePerimeterInd
        self.goalBlockInd        = goalBlockInd

    def isCellPosValid(self, rowInd, colInd):
        if 0 <= min(rowInd, colInd) and \
           rowInd < self.height     and \
           colInd < self.width:
            return True
        return False

    # adds block with one side len equal to one and other equal to passed parameter
    # (row, col) - position of top left corner of rectangle
    def addBlock(self, block) -> None:
        deltaRow, deltaCol = BlockTraverseDir.DIRECTION_DOWN.value
        if block.isHorizontal:
            deltaRow, deltaCol = BlockTraverseDir.DIRECTION_RIGHT.value

        self.numberOfBlocks += 1
        row = block.rowPos
        col = block.colPos
        for _ in range(block.sideLen):
            if not self.isCellPosValid(row, col): # check if cell position is valid
                print(BLOCK_DSNT_FIT_ERR_MSG)
                assert False

            self.board[row][col] = self.numberOfBlocks
            row += deltaRow
            col += deltaCol

    def getGateIndCellCoords(self):
        ind = self.escGatePerimeterInd
        bound = self.width + self.height + 3
        if ind >= bound:
            ind = ind - bound
            row = min(self.height + self.width - ind + 1, self.height)
            col = max(self.width - ind, 0)
            return row, col
        else:
            row = max(ind - self.width - 1, 0)
            col = min(ind, self.width + 1)
            return row, col


    def isFinalState(self) -> bool:
        gateRow, gateCol = self.getGateIndCellCoords()
        row, col = 0, 0
        for row in range(self.height):
            wasBreak = False
            for col in range(self.width):
                if self.board[row][col] == self.goalBlockInd:
                    wasBreak = True
                    break
            if wasBreak:
                break
        #print(f"row : {row}, col : {col}, gateRow : {gateRow}, gateCol : {gateCol}")
        row += 1
        col += 1

        deltaRow, deltaCol = getDirectionBy2Cells(row, col, gateRow, gateCol)
        #print(deltaRow, deltaCol)
        while self.isCellPosValid(row - 1, col - 1):
            #print("row, col : ", row, col)
            blockInd = self.board[row - 1][col - 1]
            if blockInd not in (EMPTY_CELL_BLOCK_IND, self.goalBlockInd):
                return False

            row += deltaRow
            col += deltaCol

        return row == gateRow and col == gateCol



    def getBgStyleForCell(self, rowInd, colInd):
        # cell is inside board and not on the edge
        if self.isCellPosValid(rowInd - 1, colInd - 1):
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

    def __hash__(self):
        # we use this function only in BFS algo, so basically we don't care about
        # width, height, numberOfBlocks, escGatePerimeterInd, goalBlockInd as they are invariant and
        # same for all boards that we can reach from initial one
        # so we just need to hash matrix of strings

        data = dumps(self.board, sort_keys=True).encode("utf-8")
        # return sha256(data).hexdigest()
        hashBytes = sha256(data).digest()
        # we truncate this number to only 64-bit integer
        hash = int.from_bytes(hashBytes[:8], byteorder="big")
        return hash


    def __eq__(self, other):
        return isinstance(other, BoardState) and \
               self.board == other.board

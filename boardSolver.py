from copy import deepcopy

from boardState.boardState import BoardState
from boardState.constants import EMPTY_CELL_BLOCK_IND
from enum import Enum
from collections import deque
from blockStruct import Block, BlockDirs
from terminalScreen import clearTerminal


class Directions(Enum):
    Up    = (-1,  0)
    Right = ( 0,  1)
    Down  = ( 1,  0)
    Left  = ( 0, -1)

# def getDirectionByDeltas(dx, dy) -> (int, int):
#     for dir in Directions:
#         if dir.value == (dx, dy):
#             return dir.name
#
#     # unknown direction
#     assert False

class Move:
    def __init__(self, blockInd, direction, step):
        self.blockInd  = blockInd
        self.direction = direction
        self.step      = step

def isBlockInCell(board, rowInd, colInd, blockInd) -> bool:
    # if out of board's bound or cell is empty, then there's no block in this cell
    blockInCell = board.board[rowInd][colInd]
    if not board.isCellPosValid(rowInd, colInd) or \
       blockInCell == EMPTY_CELL_BLOCK_IND:
            return False

    return blockInCell == blockInd


# returns direction, BlockDirs field: 'h' or 'v'
def getBlockDirection(board, rowInd, colInd, blockInd) -> str:
    # just in case checking that cell is valid
    assert isBlockInCell(board, rowInd, colInd, blockInd)

    if isBlockInCell(board, rowInd - 1, colInd, blockInd) or \
       isBlockInCell(board, rowInd + 1, colInd, blockInd):
            return BlockDirs.VERTICAL
    return BlockDirs.HORIZONTAL


def markBlockCellsAsVisited(
    board, row, col, blockInd, deltaRow, deltaCol, isVisited
) -> (int, int):
    isVisited[row][col] = True
    # moving while we are inside board, and it's still our block
    while board.isCellPosValid(row + deltaRow, col + deltaCol) and \
          board.board[row + deltaRow][col + deltaCol] == blockInd:
        row += deltaRow
        col += deltaCol
        assert not isVisited[row][col]
        isVisited[row][col] = True
    return row, col


def addNeighbsOfBoardToQueue(
    curBoard, block, deltaRow, deltaCol,
    previousMove4Board, queue
) -> None:
    movStep = 0
    nxtBoard = deepcopy(curBoard)
    row, col = block.rowPos, block.colPos
    #print(block.blockInd, block.sideLen, row, col)
    while curBoard.isCellPosValid(row + deltaRow, col + deltaCol) and \
          curBoard.board[row + deltaRow][col + deltaCol] == EMPTY_CELL_BLOCK_IND:
        row += deltaRow
        col += deltaCol
        movStep += 1
        nxtBoard.board[row][col] = block.blockInd
        nxtBoard.board[row - deltaRow * block.sideLen] \
                      [col - deltaCol * block.sideLen] = EMPTY_CELL_BLOCK_IND

        # if nxtBoard has not been visited
        pushableBoard = deepcopy(nxtBoard)
        if pushableBoard not in previousMove4Board:
            # previousMove4Board[nxtBoard] = Move(
            #     block.blockInd, getDirectionByDeltas(dx, dy), movStep
            # )
            previousMove4Board[pushableBoard] = Move(
                block.blockInd, (deltaRow, deltaCol), movStep
            )
            queue.append(pushableBoard)


class BoardSolver:
    def __init__(self, initialState):
        self.movesHistory     = []
        self.width            = initialState.width
        self.height           = initialState.height
        self.initialState     = initialState
        self.finalBoardState  = None

    def findBlocks4Board(self, board):
        blocks = []
        isVisited = [[False for j in range(self.width)] for i in range(self.height)]

        # clearTerminal()
        # board.displayBoardState()

        for row in range(self.height):
            for col in range(self.width):
                blockInd = board.board[row][col]
                if isVisited[row][col] or \
                   blockInd == EMPTY_CELL_BLOCK_IND:
                    continue

                dir = getBlockDirection(board, row, col, blockInd)
                # top left corner is already found because of
                # how this 2 loops iterate through cells: from top to bottom and from left to right
                # to find block len we need to go either down or right
                deltaRow, deltaCol = (Directions.Down if (dir == BlockDirs.VERTICAL) else Directions.Right).value
                #print(f"blockInd: {blockInd}, deltaRow: {deltaRow}, deltaCol: {deltaCol}, dir: {dir}")

                # moving in opposite direction
                row2, col2 = markBlockCellsAsVisited(
                    board, row, col, blockInd, deltaRow, deltaCol, isVisited
                )
                #print(row, col, row2, col2)
                sideLen = abs(row2 - row) + abs(col2 - col) + 1
                block = Block(
                    row, col, dir == BlockDirs.HORIZONTAL, sideLen, blockInd
                )
                blocks.append(block)

        return blocks


    def solveTheBoard(self):
        # we will use BFS algorithm to find solution
        previousMove4Board = dict()
        # just a fictive move, that actually didn't happen
        previousMove4Board[self.initialState] = Move(0, 0, 0)
        queue = deque()
        queue.append(deepcopy(self.initialState))

        while len(queue):
            curBoard = queue.popleft()
            blocks = self.findBlocks4Board(curBoard)
            #print("previousMove4Board: ", len(previousMove4Board))

            if curBoard.isFinalState():
                curBoard.displayBoardState()
                exit(0)

            # if len(previousMove4Board) > 5:
            #     bruh = []
            #     for key, board in previousMove4Board.items():
            #         print(key, board)
            #         bruh.append(key)
            #     bruh[3].displayBoardState()
            #     bruh[4].displayBoardState()
            #     print(bruh[3].__hash__(), bruh[4].__hash__(), bruh[3] == bruh[4])
            #     exit(0)

            for block in blocks:
                deltaRow, deltaCol = (Directions.Left if block.isHorizontal else Directions.Up).value
                # print(f"blockInd : {block.blockInd}, row : {block.rowPos}, col : {block.colPos}, sideLen : {block.sideLen}")
                # continue

                addNeighbsOfBoardToQueue(
                    curBoard, block, deltaRow, deltaCol,
                    previousMove4Board, queue
                )
                # moving in opposite direction
                block.rowPos -= (block.sideLen - 1) * deltaRow
                block.colPos -= (block.sideLen - 1) * deltaCol
                addNeighbsOfBoardToQueue(
                    curBoard, block, -deltaRow, -deltaCol,
                    previousMove4Board, queue
                )
            #exit(0)

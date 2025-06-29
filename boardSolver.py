from copy import deepcopy
from blockStruct import Block, BlockDirs
from boardState.constants import EMPTY_CELL_BLOCK_IND
from collections import deque
from enum import Enum
from inputInitialBoardState.inputInitialBoardState import updateBoardImage
from terminalScreen import clearTerminal, saveCursorPos, restoreCursorPos
import time


NUM_OF_BLINKS            = 2
BLINK_DELAY              = 0.5
WAIT_FOR_ANY_KEY_MSG     = "Print enter to continue: "
PUZZLE_IS_SOLVABLE_MSG   = ""
PUZZLE_IS_UNSOLVABLE_MSG = "Puzzle is unsolvable :(\n"


class Directions(Enum):
    Up    = (-1,  0)
    Right = ( 0,  1)
    Down  = ( 1,  0)
    Left  = ( 0, -1)


class Move:
    def __init__(self, blockInd, direction, step):
        self.blockInd  = blockInd
        self.direction = direction
        self.step      = step


def isBlockIndInCell(board, rowInd, colInd, blockInd) -> bool:
    # if out of board's bound or cell is empty, then there's no block in this cell
    if not board.isCellPosValid(rowInd, colInd):
        return False
    return board.board[rowInd][colInd] == blockInd


# returns direction, BlockDirs field: 'h' or 'v'
def getBlockDirection(board, rowInd, colInd, blockInd) -> str:
    # just in case checking that cell is valid
    assert isBlockIndInCell(board, rowInd, colInd, blockInd)

    if isBlockIndInCell(board, rowInd - 1, colInd, blockInd) or \
       isBlockIndInCell(board, rowInd + 1, colInd, blockInd):
            return BlockDirs.VERTICAL
    return BlockDirs.HORIZONTAL


def getCellsInBlock(board, blockInd) -> list[tuple[int, int]]:
    row, col = board.getBlockTopLeftCornerPos(blockInd)
    dir = getBlockDirection(board, row, col, blockInd)
    deltaRow, deltaCol = (Directions.Down if (dir == BlockDirs.VERTICAL) else Directions.Right).value

    cells = []
    while board.isCellPosValid(row, col) and \
          board.board[row][col] == blockInd:
        cells.append((row, col))
        row += deltaRow
        col += deltaCol
    return cells


def markBlockCellsAsVisited(
    board, blockInd, isVisited
) -> (int, int):
    cells = getCellsInBlock(board, blockInd)
    for (row, col) in cells:
        assert not isVisited[row][col]
        isVisited[row][col] = True
    return cells[-1]


def addNeighbsOfBoardToQueue(
    curBoard, block, deltaRow, deltaCol,
    previousMove4Board, queue
) -> None:
    movStep = 0
    nxtBoard = deepcopy(curBoard)
    row, col = block.rowPos, block.colPos
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
            previousMove4Board[pushableBoard] = Move(
                block.blockInd, (-deltaRow, -deltaCol), movStep
            )
            queue.append(pushableBoard)


def waitForAnyKey():
    input(WAIT_FOR_ANY_KEY_MSG)


class BoardSolver:
    def __init__(self, initialState):
        self.boardsHistory    = []
        self.movesHistory     = []
        self.width            = initialState.width
        self.height           = initialState.height
        self.initialState     = initialState
        self.finalBoardState  = None


    def findBlocks4Board(self, board):
        blocks = []
        isVisited = [[False for j in range(self.width)] for i in range(self.height)]

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

                # moving in opposite direction
                row2, col2 = markBlockCellsAsVisited(
                    board, blockInd, isVisited
                )
                sideLen = abs(row2 - row) + abs(col2 - col) + 1
                block = Block(
                    row, col, dir == BlockDirs.HORIZONTAL, sideLen, blockInd
                )
                blocks.append(block)

        return blocks


    def restoreHistoryOfBoards(self, previousMove4Board):
        curBoard = deepcopy(self.finalBoardState)
        while curBoard != self.initialState:
            # print("curBoard:")
            # curBoard.displayBoardState()

            move = previousMove4Board[curBoard]
            self.boardsHistory.append(deepcopy(curBoard))
            self.movesHistory.append(deepcopy(move))
            blockInd = move.blockInd
            cells = getCellsInBlock(curBoard, blockInd)
            for row, col in cells:
                curBoard.board[row][col] = EMPTY_CELL_BLOCK_IND

            deltaRow = move.direction[0] * move.step
            deltaCol = move.direction[1] * move.step
            newBlock = Block(
                cells[0][0] + deltaRow,
                cells[0][1] + deltaCol,
                cells[0][0] == cells[-1][0],
                len(cells), blockInd
            )
            assert curBoard.try2AddBlock(newBlock)

        self.boardsHistory.append(deepcopy(self.initialState))
        # reverse the array
        self.boardsHistory = self.boardsHistory[::-1]
        self.movesHistory  = self.movesHistory [::-1]


    def replayHistoryOfBoards(self):
        # +1 move, because you also need to swipe highlighted block out of the puzzle
        print(f"There are {len(self.movesHistory) + 1} moves in the most optimal solution.")
        print(f"Now, watch carefully at the board and repeat the moves.")
        waitForAnyKey()

        clearTerminal()
        self.boardsHistory[0].displayBoardState()
        for i in range(len(self.boardsHistory) - 1):
            blockInd = self.movesHistory[i].blockInd
            cells = getCellsInBlock(self.boardsHistory[i], blockInd)

            # blink with block that is going to be moved
            time.sleep(BLINK_DELAY)
            for _ in range(NUM_OF_BLINKS):
                saveCursorPos()
                for row, col in cells:
                    self.boardsHistory[i].updateCellAndRedrawIt(row, col, EMPTY_CELL_BLOCK_IND)
                restoreCursorPos()
                time.sleep(BLINK_DELAY)

                saveCursorPos()
                for row, col in cells:
                    self.boardsHistory[i].updateCellAndRedrawIt(row, col, blockInd)
                restoreCursorPos()
                time.sleep(BLINK_DELAY)

            time.sleep(BLINK_DELAY)
            updateBoardImage(self.boardsHistory[i],
                             self.boardsHistory[i + 1])


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

            if curBoard.isFinalState():
                print(PUZZLE_IS_SOLVABLE_MSG)
                self.finalBoardState = deepcopy(curBoard)
                self.restoreHistoryOfBoards(previousMove4Board)
                break

            for block in blocks:
                deltaRow, deltaCol = (Directions.Left if block.isHorizontal else Directions.Up).value

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
        else:
            print(PUZZLE_IS_UNSOLVABLE_MSG)
            exit(0)

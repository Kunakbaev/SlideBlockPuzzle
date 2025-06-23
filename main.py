from enum import Enum

# ansi escape sequences
class TerminalColor(Enum):
    NORMAL = "\x1b[0m"
    GREEN  = "\x1b[1;99;42m"
    RED    = "\x1b[1;39;41m"
    BORDER = "\x1b[1;39;40m#\x1b[0m"

EMPTY_CELL_BLOCK_IND  = 0
# actually, I don't use it for now.
# It's equal to 1, because in ansi colors decimal codes that end with 1 represent red color
HIGHLIGHTED_BLOCK_IND = 1

class Block:
    def __init__(self, rowPos, colPos, isHorizontal, sideLen):
        self.rowPos       = rowPos
        self.colPos       = colPos
        self.isHorizontal = isHorizontal
        self.sideLen      = sideLen

def getBlockColorStyle(blockInd) -> str:
    # we iterate through colors in reverse order,
    # as we want bright and pretty colors to go first
    blockInd -= 2 # as we already spent 2 colors: black for empty cell and red for goal block
    backgroundCode = 107 - (blockInd % 8)
    backgroundCode -= (blockInd >= 8) * 60

    if blockInd + 2 == HIGHLIGHTED_BLOCK_IND: # that's a goal block
        backgroundCode = 41
    if blockInd + 2 == EMPTY_CELL_BLOCK_IND:
        backgroundCode = 40
    return f"\x1b[1;39;{backgroundCode}m \x1b[0m"

class BoardState:
    def __init__(self, width, height, gatePerimeterInd, goalBlockInd):
        self.width            = width
        self.height           = height
        self.board            = [[EMPTY_CELL_BLOCK_IND for j in range(width)] for i in range(height)]
        self.numberOfBlocks   = 0 # counts how many are already on the board
        self.gatePerimeterInd = gatePerimeterInd
        self.goalBlockInd     = goalBlockInd

    # adds block with one side len equal to one and other equal to passed parameter
    # (rowPos, colPos) - position of top left corner of rectangle
    def addBlock(self, block) -> None:
        dx, dy = (1, 0) if block.isHorizontal else (0, 1)

        self.numberOfBlocks += 1
        rowPos = block.rowPos
        colPos = block.colPos
        for _ in range(block.sideLen):
            if min(rowPos, colPos) < 0 or \
               rowPos >= self.height   or \
               colPos >= self.width: # check if cell position is valid
                print("Error: block doesn't fit on the board")
                assert False

            self.board[rowPos][colPos] = self.numberOfBlocks
            rowPos += dy
            colPos += dx

    def isFinalState(self, gatePerimeterInd, goalBlockInd) -> bool:
        pass

    def displayBoardState(self, highlightBlockInd, highlightColor):
        h = self.height * 2 + 1
        w = self.width  * 4 + 1
        result = [['-' for j in range(w)] for i in range(h)]

        for colInd in range(0, w, 4):
            for rowInd in range(1, h, 2):
                result[rowInd][colInd] = '|'

        for colInd in range(0, self.width):
            for rowInd in range(0, self.height):
                i = rowInd * 2 + 1
                j = colInd * 4 + 2

                word = str(self.board[rowInd][colInd])
                result[i][j] = word
                result[i][j - 1] = result[i][j + 1] = ' '
                if len(word) == 2:
                    result[i][j - 1] = word[0]
                    result[i][j    ] = word[1]

        # print("\nBoard state:")
        # for i in range(len(result)):
        #     # print(*result[i], sep='')
        #     for j in range(len(result[i])):
        #         isNeededBlock = False
        #         if j % 4 == 1 or j % 4 == 2:
        #             ind = j // 4 * 4 + 1
        #             firstChar  = result[i][ind]
        #             secondChar = result[i][ind + 1]
        #
        #             isNeededBlock = (firstChar == ' ' and secondChar == str(highlightBlockInd)) or \
        #                                     (firstChar + secondChar) == str(highlightBlockInd)
        #
        #
        #         add = highlightColor.value if (isNeededBlock and result[i][j] != ' ') else ""
        #         print(add + result[i][j] + TerminalColor.NORMAL.value, end='')
        #     print()
        # print()

        # print("\nBoard state:")
        # for i in range(self.height):
        #     for j in range(self.width):
        #         isNeededBlock = False
        #         if j % 4 == 1 or j % 4 == 2:
        #             ind = j // 4 * 4 + 1
        #             firstChar = result[i][ind]
        #             secondChar = result[i][ind + 1]
        #
        #             isNeededBlock = (firstChar == ' ' and secondChar == str(highlightBlockInd)) or \
        #                             (firstChar + secondChar) == str(highlightBlockInd)
        #
        #         add = highlightColor.value if (isNeededBlock and result[i][j] != ' ') else ""
        #         print(add + str(self.board[i][j]) + TerminalColor.NORMAL.value, end='')
        #     print()
        # print()

        print("\nBoard state:")
        # WARNING: should be an integer
        # actually it's just a side length of one block tile
        SCALE_FACTOR = 3
        for i in range((self.height + 2) * SCALE_FACTOR):
            rowInd = i // SCALE_FACTOR
            for j in range((self.width + 2) * SCALE_FACTOR):
                colInd = j // SCALE_FACTOR

                # is cell located on perimeter of grid?
                if min(rowInd, colInd) == 0  or \
                   rowInd == self.height + 1 or \
                   colInd == self.width  + 1:
                    perimeterCellInd = rowInd + colInd
                    if rowInd == self.height + 1 or \
                      (colInd == 0 and rowInd != 0):
                        perimeterCellInd = (self.width + self.height + 2) * 2 - perimeterCellInd
                    #print(rowInd, colInd, perimeterCellInd)
                    blockColorStyle = TerminalColor.BORDER.value
                    if perimeterCellInd == self.gatePerimeterInd:
                        blockColorStyle = " "
                    # we print it twice as line height is approximately equal to char width * 2
                    print(blockColorStyle * 2, end='')
                    continue

                blockInd = int(self.board[rowInd - 1][colInd - 1])
                blockColorStyle = getBlockColorStyle(blockInd)
                print(blockColorStyle * 2, end='')
            print()
        print()




class BoardSolver:
    def __init__(self, width, height, gatePerimeterInd, goalBlockInd, initialState):
        self.movesHistory     = []
        self.width            = width
        self.height           = height
        self.gatePerimeterInd = gatePerimeterInd
        self.goalBlockInd     = goalBlockInd
        self.initialState     = initialState

    def solveTheBoard(self):
        pass


if __name__ == "__main__":
    print("Available colors:")

    for i in range(16):
        code = 40 + (i % 8)
        code += (i >= 8) * 60
        print(f"\x1b[1;39;{code}m \x1b[0m", end='')

    #exit(0)

    initialBoardState = BoardState(6, 6, 10, 1)

    # WARNING:
    # make sure, that your goal block, that will escape the puzzle is located on the first place (in one indexation)
    initBoardsBlocks = [
        Block(2, 0, True,  2),
        Block(0, 0, False, 2),
        Block(3, 1, False, 2),
        Block(4, 2, False, 2),
        Block(0, 4, False, 3),
        Block(2, 5, False, 3),
        Block(0, 2, True,  2),
        Block(3, 2, True,  2),
        Block(4, 3, True,  2),
        Block(3, 2, True,  2),
    ]

    for block in initBoardsBlocks:
        initialBoardState.addBlock(block)
    initialBoardState.displayBoardState(10, TerminalColor.RED)



from boardState.boardState import BoardState
from boardState.constants  import HIGHLIGHTED_BLOCK_IND
from blockStruct           import Block, BlockDirs
from boardSideTypes        import *
from copy                  import deepcopy
from inputInitialBoardState.constants import *
from terminalScreen        import replacePrevLineWithMsg, saveCursorPos, restoreCursorPos, clearTerminal


# returns string repr of error if word is not natural number, or it's too big
# otherwise returns int(word)
def tryToReadNaturalNum(
        word,
        maxValue    = MAX_INPUT_INT_VALUE,
        maxValueErr = ReadNaturalNumFuncErrMsgs.NUMBER_TOO_BIG
) -> (int, str):
    if not word.isdigit():
        return -1, ReadNaturalNumFuncErrMsgs.NOT_A_NUMBER

    number = int(word)
    if number <= 0:
        return -1, ReadNaturalNumFuncErrMsgs.NOT_A_NATURAL_NUM
    if number > maxValue:
        return -1, maxValueErr
    return number, ReadNaturalNumFuncErrMsgs.ALL_FINE_MSG


def readIntegerSafely(
        message,
        maxValue=MAX_INPUT_INT_VALUE,
        maxValueErr=ReadNaturalNumFuncErrMsgs.NUMBER_TOO_BIG
) -> int:
    while True:
        print(message, end="")
        word = input()
        number, err = tryToReadNaturalNum(word, maxValue, maxValueErr)
        if err == ReadNaturalNumFuncErrMsgs.ALL_FINE_MSG:
            break

        replacePrevLineWithMsg(err)

    return number


def readExitGatePos(width, height) -> int:
    print(InputPrompts.EXIT_GATE_HELP_MSG)

    ind = -1
    while True:
        print(InputPrompts.EXIT_GATE_INPUT_PROMPT, end="")
        line = input()
        if len(line.split(' ')) != 2:
            replacePrevLineWithMsg(ReadExitGateFuncErrMsgs.INVALID_NUM_OF_ARGS)
            continue

        sideType, gateIndWord = line.split(' ')
        if not isValidSideType(sideType):
            replacePrevLineWithMsg(ReadExitGateFuncErrMsgs.INVALID_SIDE_TYPE)
            continue

        gateInd, err = tryToReadNaturalNum(gateIndWord)
        if err != ReadNaturalNumFuncErrMsgs.ALL_FINE_MSG:
            replacePrevLineWithMsg(err)
            continue

        # gate index is bigger than side len
        if (isHorizontalSideType(sideType) and gateInd > width) or \
           (  isVerticalSideType(sideType) and gateInd > height):
                replacePrevLineWithMsg(ReadExitGateFuncErrMsgs.GATE_IND_TOO_BIG)
                continue

        # calculating perimeter index
        if   sideType == BoardSideTypes.TOP:
            ind = gateInd
        elif sideType == BoardSideTypes.RIGHT:
            ind = gateInd + width + 1
        elif sideType == BoardSideTypes.BOTTOM:
            ind = 2 * width - gateInd + height + 3
        elif sideType == BoardSideTypes.LEFT:
            ind = 2 * (width + height) - gateInd + 4
        else: assert False # actually, we already checked that sideType is valid, but just in case
        break

    print(ind)
    assert ind != -1
    return ind


def readInitialBoardConfiguration() -> BoardState:
    width       = readIntegerSafely(
        InputPrompts.BOARD_WIDTH_INPUT_PROMPT,
        MAX_BOARD_WIDTH,
        ReadNaturalNumFuncErrMsgs.BOARD_WIDTH_TOO_BIG
    )
    height      = readIntegerSafely(
        InputPrompts.BOARD_HEIGHT_INPUT_PROMPT,
        MAX_BOARD_HEIGHT,
        ReadNaturalNumFuncErrMsgs.BOARD_HEIGHT_TOO_BIG
    )
    scaleFactor = readIntegerSafely(
        InputPrompts.BOARD_SCALE_FACTOR_INPUT_PROMPT,
        MAX_BOARD_SCALE_FACTOR,
        ReadNaturalNumFuncErrMsgs.BOARD_SCL_FACTOR_TOO_BIG
    )
    gatePerimeterInd = readExitGatePos(width, height)

    initialBoard = BoardState(width, height, scaleFactor, gatePerimeterInd, HIGHLIGHTED_BLOCK_IND)
    return initialBoard


# asks user to input new blocks configuration
# repeats this process until configuration is correct or there are no blocks to input
# "-" or Enter is inputted
# returns: bool, whether another block was read or user ended process of blocks input
def readAndAddNewBlock(initialBoard) -> BlockReadState:
    width  = initialBoard.width
    height = initialBoard.height

    while True:
        print(InputPrompts.READ_NEW_BLOCK_INPUT_PROMPT, end="")
        line = input()

        if line == BlockReadCommands.UNDO:
            return BlockReadState.UNDO_COMMAND
        if line in (BlockReadCommands.END_INPUT1,
                    BlockReadCommands.END_INPUT2):
            return BlockReadState.INPUT_END # new block was NOT added

        if initialBoard.numberOfBlocks >= MAX_NUMBER_OF_BLOCKS:
            replacePrevLineWithMsg(ReadNewBlockFuncErrMsgs.TOO_MANY_BLOCKS)
            continue

        if len(line.split()) != READ_NEW_BLOCK_NUM_OF_ARGS:
            replacePrevLineWithMsg(ReadNewBlockFuncErrMsgs.INVALID_NUM_OF_ARGS)
            continue

        colWord, rowWord, blockDir, sideLenWord = line.split(' ')
        col, err = tryToReadNaturalNum(colWord)
        if err != ReadNaturalNumFuncErrMsgs.ALL_FINE_MSG:
            replacePrevLineWithMsg(err)
            continue
        row, err = tryToReadNaturalNum(rowWord)
        if err != ReadNaturalNumFuncErrMsgs.ALL_FINE_MSG:
            replacePrevLineWithMsg(err)
            continue
        row -= 1
        col -= 1

        if not initialBoard.isCellPosValid(row , col):
            replacePrevLineWithMsg(ReadNewBlockFuncErrMsgs.INVALID_COORDS)
            continue

        if blockDir not in (BlockDirs.HORIZONTAL,
                            BlockDirs.VERTICAL):
            replacePrevLineWithMsg(ReadNewBlockFuncErrMsgs.INVALID_BLOCK_DIR)
            continue

        sideLen, err = tryToReadNaturalNum(sideLenWord)
        if err != ReadNaturalNumFuncErrMsgs.ALL_FINE_MSG:
            replacePrevLineWithMsg(err)
        if (blockDir == BlockDirs.HORIZONTAL and col + sideLen - 1 >= width) or \
           (blockDir == BlockDirs.VERTICAL   and row + sideLen - 1 >= height):
                replacePrevLineWithMsg(ReadNewBlockFuncErrMsgs.BLOCK_DSNT_FIT)
                continue

        if sideLen < MIN_BLOCK_SIDE_LEN:
            replacePrevLineWithMsg(ReadNewBlockFuncErrMsgs.BLOCK_LEN_TOO_SMALL)
            continue

        block = Block(
            row, col, blockDir == BlockDirs.HORIZONTAL, sideLen,
            initialBoard.numberOfBlocks + 1
        )

        # that's a bit expensive, but boards are small, so that's okay
        boardCopy = deepcopy(initialBoard.board)
        hasAdded = initialBoard.try2AddBlock(block)

        if hasAdded and initialBoard.isGoalBlockInRightDir():
            break

        errMessage = ReadNewBlockFuncErrMsgs.BLOCK_DSNT_FIT if not hasAdded \
                else ReadNewBlockFuncErrMsgs.GOAL_BLOCK_WRONG_DIR

        initialBoard.board = deepcopy(boardCopy)
        initialBoard.numberOfBlocks -= 1
        replacePrevLineWithMsg(errMessage)

    return BlockReadState.NEW_BLOCK_ADDED # new block was added


# double bufferization technique
def updateBoardImage(oldBoard, newBoard) -> None:
    saveCursorPos()
    for rowInd in range(oldBoard.height):
        for colInd in range(oldBoard.width):
            old = oldBoard.board[rowInd][colInd]
            new = newBoard.board[rowInd][colInd]

            if old == new:  # nothing has changed, no need for screen update
                continue

            # matrix value is already up to date, but we need to update screen
            newBoard.updateCellAndRedrawIt(rowInd, colInd, new)
    restoreCursorPos()


def readInitialBoardState() -> BoardState:
    while True:
        initialBoard = readInitialBoardConfiguration()
        initialBoard.displayBoardState()
        print(InputPrompts.BOARD_CONFIG_VALIDATION_INPUT_PROMPT, end="")
        answer = input()
        if answer == BOARD_CONFIG_VALIDATION_OK_ANS:
            break
        clearTerminal()

    clearTerminal()
    initialBoard.displayBoardState()

    print(InputPrompts.READ_INIT_BOARD_STATE_HELP_MSG)
    blockReadState = BlockReadState.NEW_BLOCK_ADDED
    # That's not very efficient to store actual boards and not changes that were applied to them,
    # but boards are very small, so that's okay
    # This is stack of how board have looked back in time,
    # element on the bottom (first added one) is just empty board,
    # so you can't undo further than that
    # user can type undo command and restore
    historyOfBoards = [deepcopy(initialBoard)]
    isFirstIteration = True
    while blockReadState != BlockReadState.INPUT_END:
        if not isFirstIteration:
            # we don't want to stack input message, so we replace previous one
            replacePrevLineWithMsg("", addSep=False) # this actually just clears previous line
        isFirstIteration = False

        initialBoard = deepcopy(historyOfBoards[-1])
        blockReadState = readAndAddNewBlock(initialBoard)

        if blockReadState == BlockReadState.UNDO_COMMAND:
            if len(historyOfBoards) > 1:
                # redraw old board
                # initialBoard.displayBoardState(1, 1)
                # historyOfBoards[-2].displayBoardState(1, 1)
                updateBoardImage(initialBoard, historyOfBoards[-2])
                initialBoard = historyOfBoards[-2]
                historyOfBoards.pop()
            continue

        updateBoardImage(historyOfBoards[-1], initialBoard)
        historyOfBoards.append(deepcopy(initialBoard))

    return initialBoard

"""

Configuration of one of the levels from MoveTheBlock game on my phone
6
6
3
right 3
yes
1 3 h 2
1 1 v 2
3 1 h 2
2 2 h 3
5 1 v 3
2 4 v 2
3 4 h 2
3 5 v 2
4 5 h 2
6 3 v 3


6
6
right 3
yes
1 3 h 2
3 1 v 3
5 1 h 2
4 2 v 3
5 2 h 2
1 4 v 2
2 4 h 2
5 4 h 2
4 6 h 2
6 5 v 2

6
6
2
bottom 4
yes
4 1 v 2
5 1 h 2
2 2 h 2
1 3 h 2
5 2 v 3
6 3 v 2
3 3 v 2
2 4 v 2
2 6 h 3
4 5 h 3







6
6
3
right 3
yes
1 3 h 2
1 1 h 3
1 2 h 2
3 2 v 2
4 1 v 2
6 1 v 2
6 3 v 2
1 4 v 2
2 4 h 2
4 4 h 2
3 5 h 2
5 5 h 2
1 6 h 3


"""

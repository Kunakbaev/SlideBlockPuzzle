from terminalScreen import clearTerminal
from inputInitialBoardState.inputInitialBoardState import readInitialBoardState
from boardSolver import BoardSolver
from copy import deepcopy

if __name__ == "__main__":
    # print("Available colors:")
    #
    # for i in range(16):
    #     code = 40 + (i % 8)
    #     code += (i >= 8) * 60
    #     print(f"\x1b[1;39;{code}m \x1b[0m", end='')

    #exit(0)

    # initialBoardState = BoardState(6, 6, 10, 1)
    #
    # # WARNING:
    # # make sure, that your goal block, that will escape the puzzle is located on the first place (in one indexation)
    # initBoardsBlocks = [
    #     Block(2, 0, True,  2),
    #     Block(0, 0, False, 2),
    #     Block(3, 1, False, 2),
    #     Block(4, 2, False, 2),
    #     Block(0, 4, False, 3),
    #     Block(2, 5, False, 3),
    #     Block(0, 2, True,  2),
    #     Block(3, 2, True,  2),
    #     Block(4, 3, True,  2),
    #     Block(3, 2, True,  2),
    # ]
    #
    # for block in initBoardsBlocks:
    #     initialBoardState.addBlock(block)




    clearTerminal()
    initialBoardState = readInitialBoardState()
    clearTerminal()
    initialBoardState.displayBoardState()

    # isFinalState = initialBoardState.isFinalState()
    # print(isFinalState)

    # cop = deepcopy(initialBoardState)
    # cop.board[0][0] = 0
    # cop.board[0][0] = 2
    # print(f"InitialBoard: hash={initialBoardState.__hash__()}")
    # print(f"copy        : hash={cop.__hash__()}")
    # print("Are they equal : ", cop == initialBoardState)
    # exit(0)

    boardSolver = BoardSolver(initialBoardState)
    boardSolver.solveTheBoard()


    #initialBoardState.displayBoardState(10, TerminalColor.RED)

    # oldValue = initialBoardState.board[0][0]
    # newValue = 0
    # BLINK_DELAY = 0.8
    # for i in range(2):
    #     if i: initialBoardState.updateCellValue(0, 0, oldValue)
    #     moveCursorToPos(SCALE_FACTOR * (initialBoardState.height + 2) + 2, 0)
    #     time.sleep(BLINK_DELAY)
    #
    #     initialBoardState.updateCellValue(0, 0, newValue)
    #     moveCursorToPos(SCALE_FACTOR * (initialBoardState.height + 2) + 2, 0)
    #     time.sleep(BLINK_DELAY)
    #
    #
    # moveCursorToPos(SCALE_FACTOR * (initialBoardState.height + 2) + 2, 0)
    #initialBoardState.displayBoardState(10, TerminalColor.RED)
    # initialBoardState.displayBoardState(10, TerminalColor.RED)

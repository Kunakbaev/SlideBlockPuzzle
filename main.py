from boardSolver import BoardSolver
from inputInitialBoardState.inputInitialBoardState import readInitialBoardState
from terminalScreen import clearTerminal

if __name__ == "__main__":
    clearTerminal()
    initialBoardState = readInitialBoardState()
    clearTerminal()
    initialBoardState.displayBoardState()

    boardSolver = BoardSolver(initialBoardState)
    boardSolver.solveTheBoard()
    boardSolver.replayHistoryOfBoards()

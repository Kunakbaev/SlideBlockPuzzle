from enum import StrEnum, IntEnum
import sys
from boardState.constants import HIGHLIGHTED_BLOCK_IND, EMPTY_CELL_BLOCK_IND

"""

WARNING:
Please read this, otherwise you probably won't understand anything in this file
About ANSI escape codes:
wiki page: https://en.wikipedia.org/wiki/ANSI_escape_code
table with colors: https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit

What does \x1b mean? (you can also see usage of \033
x - for hex positional numeral system
so 1b(hex) = 1 * 16 + 11 = 27
033 - same number but in octal

What's 27? It's char code of ESC char.

Also, this probably won't work for Windows. MacOS and Linux are somewhat similar,
so I expect there will be less problems with that.

"""

class TerminalBgCodes(IntEnum):
    BLACK_NORM = 40,
    RED_NORM   = 41,
    GREEN_NORM = 42,

# background styles (ansi escape sequences) for tiles
class TerminalBgStyles(StrEnum):
    NORMAL   = "\x1b[0m"
    GREEN    = f"\x1b[1;39;{TerminalBgCodes.GREEN_NORM}m"
    RED      = f"\x1b[1;39;{TerminalBgCodes.RED_NORM}m"
    BORDER   = f"\x1b[1;39;{TerminalBgCodes.BLACK_NORM}m#\x1b[0m"
    ESC_GATE = " " # bg style for escape gate, it's just "invisible" color

def getBlockColorStyle(blockInd) -> str:
    backgroundCode = 0
    origBlockInd = blockInd
    # we iterate through colors in reverse order,
    # as we want bright and pretty colors to go first
    if blockInd == HIGHLIGHTED_BLOCK_IND: # that's a goal block
        backgroundCode = TerminalBgCodes.RED_NORM
    elif blockInd == EMPTY_CELL_BLOCK_IND:
        backgroundCode = TerminalBgCodes.BLACK_NORM
    else:
        # there are 8 background color of types: normal and bright (so 16 in total)
        # normal bg color codes:  40-47
        # bright bg color codes: 100-107
        blockInd -= 2  # as we already spent 2 colors: black for empty cell and red for goal block
        backgroundCode = 107 - (blockInd % 8)
        # 100 - 40 = 60 -> delta in codes between bright and normal bg colors
        # first eight are bright and last eight are normal, so we subtract difference
        backgroundCode -= (blockInd >= 8) * (100 - 40)

    text = str(origBlockInd)[-1] if origBlockInd != 0 else " "
    return f"\x1b[1;30;{backgroundCode}m{text}" + TerminalBgStyles.NORMAL

def clearTerminal():
    print("\x1b[2J\x1b[H", end="", flush=True)

def moveCursorToPos(row, col):
    print(f"\x1b[{row};{col}H", end="", flush=True)

def saveCursorPos():
    print("\x1b[s", end="", flush=True)

def restoreCursorPos():
    print("\x1b[u", end="", flush=True)

# addSep - additional parameter, by default is set to True
# True  -> adds sep after message equal to ". "
# False -> just prints message
def replacePrevLineWithMsg(msg, addSep=True):
    print("\x1b[F",  end="") # move cursor one line up
    print("\x1b[2K", end="") # completely clear previous line
    print(msg, end=". " if addSep else "")
    sys.stdout.flush()

from enum import Enum, StrEnum


MAX_INPUT_INT_VALUE            = 50
READ_NEW_BLOCK_NUM_OF_ARGS     = 4
BOARD_CONFIG_VALIDATION_OK_ANS = "yes"


class InputPrompts(StrEnum):
    EXIT_GATE_HELP_MSG                  = """
You need to specify, where gate, through which block needs to exit, is located.
To do so, input in following configuration: side gateInd
side type - can be one of the following: {"top", "right", "bottom", "left"}
gateInd   - what's index of exit gate. If side type is "top" or "bottom" than index is counted from left to right. Otherwise, it's counted from top to bottom.
    """
    EXIT_GATE_INPUT_PROMPT               = "Input side type and gate index: "
    BOARD_WIDTH_INPUT_PROMPT             = "Input board width: "
    BOARD_HEIGHT_INPUT_PROMPT            = "Input board height: "
    READ_NEW_BLOCK_INPUT_PROMPT          = "Input block configuration: "
    BOARD_CONFIG_VALIDATION_INPUT_PROMPT = "Is this correct board configuration? Print yes if so: "
    READ_INIT_BOARD_STATE_HELP_MSG       = """
Now you need to specify blocks positions on the board.
Format of each block configuration:
x y blockDir sideLen
(x, y)       - integers, coordinates of top left corner of the block
blockDir     - single char, 'h' for horizontal and 'v' for vertical
sideLen      - integer, length of a bigger block side, other one is equal to 1
If you have specified all blocks from your board configuration and wish to end input process, just print '-' or simply press Enter.
If you have done some mistakes, you can type "undo" command and restore previous board configuration
Note, that your highlighted block (one that is different from others and needs to exit the puzzle) should be first on your list.
    """


class ReadNaturalNumFuncErrMsgs(StrEnum):
    NOT_A_NUMBER      = "Error: that's not a correct natural number"
    NOT_A_NATURAL_NUM = "Error: number must be natural (positive)"
    NUMBER_TOO_BIG    = "Error: number is too big"
    ALL_FINE_MSG      = ""


class ReadExitGateFuncErrMsgs(StrEnum):
    INVALID_NUM_OF_ARGS = "Error: there should be exactly 2 arguments: side type and gate index"
    INVALID_SIDE_TYPE   = "Error: incorrect side type. Possible variants: top, right, bottom, left"
    GATE_IND_TOO_BIG    = "Error: gateInd is bigger than side len"


class ReadNewBlockFuncErrMsgs(StrEnum):
    INVALID_NUM_OF_ARGS = "Error: wrong number of arguments. Configuration looks like this: x y blockDir sideLen"
    INVALID_COORDS      = "Error: invalid coordinates of top left block corner, it's outside of the board"
    INVALID_BLOCK_DIR   = "Error: wrong block direction, it should be either 'h' for horizontal or 'v' for vertical orientation of the block"
    BLOCK_DSNT_FIT      = "Error: block doesn't fit on the board"


class BlockReadState(Enum):
    NEW_BLOCK_ADDED = 1,
    INPUT_END       = 2,
    UNDO_COMMAND    = 3


class BlockReadCommands(StrEnum):
    UNDO       = "undo",
    END_INPUT1 = "",     # simple Enter key press
    END_INPUT2 = "-"

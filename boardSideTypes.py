from enum import StrEnum


class BoardSideTypes(StrEnum):
    TOP    = "top",
    RIGHT  = "right",
    BOTTOM = "bottom",
    LEFT   = "left"


def isHorizontalSideType(sideType) -> bool:
    return sideType == BoardSideTypes.TOP or \
           sideType == BoardSideTypes.BOTTOM


def isVerticalSideType(sideType) -> bool:
    return sideType == BoardSideTypes.RIGHT or \
           sideType == BoardSideTypes.LEFT


def isValidSideType(sideType) -> bool:
    return isHorizontalSideType(sideType) or \
             isVerticalSideType(sideType)

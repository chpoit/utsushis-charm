from enum import Enum


class ParseError(Enum):
    NO_SKILL = 1
    MUST_FIX = 2
    BAD_NAME = 3

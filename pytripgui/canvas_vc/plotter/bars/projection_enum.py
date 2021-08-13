from enum import Enum


class BarProjection(Enum):
    """
    Enum class that holds all the strings that are used to register all bar classes in matplotlib
    """
    DEFAULT = 'BAR_PROJECTION_DEFAULT_NAME'
    CTX = 'ctx_bar'
    DOS = 'dos_bar'
    LET = 'let_bar'

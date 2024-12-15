"""operators.py"""
from enum import Enum


class Operators(Enum):
    """
    manages operators and their symbolic names
    """
    EQ = "="
    NE = "!="
    GT = ">"
    GE = ">="
    LT = "<"
    LE = "<="
    IN = "IN"
    NOT_IN = "NOT IN"
    LIKE = "LIKE"
    NOT_LIKE = "NOT LIKE"

    def requires_list(self):
        """
        Check if the operator requires a list of values (e.g., IN, NOT IN).
        """
        return self in {Operators.IN, Operators.NOT_IN}

    def handles_null(self):
        """
        Check if the operator handles NULL values (e.g., EQ, NE).
        """
        return self in {Operators.EQ, Operators.NE}

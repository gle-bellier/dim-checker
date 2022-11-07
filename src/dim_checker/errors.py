from typing import Any

class FormulaParenthesisError(Exception):
    """Exception raised when all parenthesis in a formula are not closed."""

    def __init__(self, formula: str, payload=None):
        self.formula = formula
        self.payload = payload 


    def __str__(self):
        return f"""The formula "{str(self.formula)}" has unclosed or empty parenthesis"""



    
class FormulaCharacterError(Exception):
    """Exception raised when a formula character is not correct."""

    def __init__(self, formula: str, character: str, payload=None):
        self.formula = formula
        self.character = character
        self.payload = payload


    def __str__(self):
        return f"""The character "{self.character}" is not valid in formula: {self.formula}."""


class ConstraintTypeError(Exception):
    """Exception raised when constraints are not integers.
    """

    def __init__(self, dim: str, value: Any, payload=None) -> None:
        self.dim = dim
        self.value = value
        

    def __str__(self):
        return f"""The constraint "{self.dim}={self.value}" must have an integer value, got {type(self.value)}."""


class ConstraintDimError(Exception):
    """Exception raised when constraints are not valid."""

    def __init__(self, dim: Any, payload=None) -> None:
        self.dim = dim
        

    def __str__(self):
        return f"""The constraint dimension "{self.dim}" must be a single letter."""
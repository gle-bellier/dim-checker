from typing import Any

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
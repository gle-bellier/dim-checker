
class PatternNumberFormulasError(Exception):
    """Exception raised when constraints are not valid."""

    def __init__(self, pattern: str, payload=None) -> None:
        self.pattern = pattern
        

    def __str__(self):
        return f"""The pattern "{self.pattern}" must have exactly two formulas separated by "->"."""
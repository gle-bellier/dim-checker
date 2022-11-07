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

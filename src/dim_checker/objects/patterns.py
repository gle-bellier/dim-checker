from dim_checker.objects.formulas import Formula
from dim_checker.errors.pattern_errors import PatternNumberFormulasError

class Pattern:

    def __init__(self, pattern: str) -> None:
        """Initializes pattern and extract formulas.

        Args:
            pattern (str): pattern string. The format of the pattern is the following:
            "input dims formula -> output dims formula". Each formula should follow this 
            formatting: 
            - include letters for each dimensions, e.g, batches of elements with 32 features 
            might be depicted by the formula "bh" and batches of 3 canals 2D pictures with 
            "bchw". 
            - you can use arithmetical expressions inside formulas such as (2*n+1). The 
            multiplication operator * must be written (2n) will raise an error. Every 
            opened parenthesis must be closed.
        """

        self.pattern = pattern
        self.in_formula, self.out_formula = self.parse_pattern(pattern)


    def __repr__(self) -> str:
        """Creates and returns description for the current pattern.

        Returns:
            str: pattern description.
        """
        return f"Pattern: {self.pattern}."

    def parse_pattern(self, pattern: str) -> list[Formula]:
        """Parses the pattern and returns input and output formulas included in pattern".

        Args:
            pattern (str): pattern of the form "in_formula -> out_formula".

        Returns:
            list[str]: results of the pattern parsing, returns in_formula and 
            out_formula as strings.
        """
        # remove spaces
        pattern = pattern.replace(" ", "")
        # split the formula
        formulas = pattern.split("->")
        # check if there are exactly two formulas
        if len(formulas)!=2:
            raise PatternNumberFormulasError(pattern)

        in_formula, out_formula = formulas
        # create in and out formulas object
        return [Formula(in_formula), Formula(out_formula)]
            



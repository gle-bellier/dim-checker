from typing import Tuple
from dim_checker.errors import FormulaCharacterError, FormulaParenthesisError


class Pattern:

    def __init__(self, pattern: str) -> None:
        """Initialize pattern and extract formulas.

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

        in_formula, out_formula = self.parse_pattern(pattern)

        self.in_dims, self.in_variables = self.parse_formula(in_formula)
        self.out_dims, self.out_variables = self.parse_formula(out_formula)

    def parse_pattern(self, pattern: str) -> list[str]:
        """Parse the pattern and return input and output formulas included in pattern".

        Args:
            pattern (str): pattern of the form "in_formula -> out_formula".

        Returns:
            Tuple[str, str]: results of the pattern parsing, returns in_formula and 
            out_formula as strings.
        """
        # remove spaces
        pattern = pattern.replace(" ", "")
        # split the formula
        return pattern.split("->")
        

            
    def parse_formula(self, formula: str) -> Tuple[list, set]:
        """Parse the formula into list of the dimensions and the set 
        of variables involved in the dimensions definitions. 

        Args:
            formula (str): input or output formula.

        Raises:
            FormulaParenthesisError: error raised if any unclosed parenthesis in the formula.
            FormulaCharacter: error raised if any unvalid character in formula.

        Returns:
            Tuple[list, set]: list of all the dimensions and set of all the 
            variables used to define the dimensions.
        """

        # list of all dims (explicit and implicit ones).
        dims = []
        # set of all the different variables needed.
        variables = set()
        # keep track of the number of opened parenthesis.
        n_par = 0
        # initialize arithmetical expression
        exp = ""

        for c in formula:
            if c == "(":
                exp += c
                n_par += 1

            elif c == ")":
                n_par -= 1
                exp += c
                # if the exp ends add it to the dimensions, else keep going.
                if n_par == 0:
                    dims += [exp]
                    # reset exp
                    exp = ""

            else:
                if n_par > 0:
                    exp += c
                    # if the caracter is a letter, it is a dimension
                    # we need to store
                    if c.isalpha():
                        variables.add(c)
                else:
                    if c.isalpha():
                        dims += [c]
                        variables.add(c)

                    else:
                        # unvalid character
                        raise FormulaCharacterError(formula, c)

        # raise error if there is unclosed parenthesis
        if n_par != 0:
            raise FormulaParenthesisError(formula)


        return dims, variables



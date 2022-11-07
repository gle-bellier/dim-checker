from typing import Tuple

from dim_checker.errors.formula_errors import FormulaCharacterError, FormulaParenthesisError 

class Formula:
    
    def __init__(self, formula:str) -> None:
        """Initializes formula object.

        Args:
            formula (str): input or output formula.
        """

        pass 

    def parse_formula(self, formula: str) -> Tuple[list[str], set[str]]:
        """Parse the formula into list of the dimensions and the set 
        of variables involved in the dimensions definitions. 

        Args:
            formula (str): input or output formula.

        Raises:
            FormulaParenthesisError: error raised if any unclosed parenthesis in the formula.
            FormulaCharacter: error raised if any unvalid character in formula.

        Returns:
            Tuple[list[str], set[str]]: list of all the dimensions and set of all the 
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
                
                # raise error if empty parenthesis
                if exp == "(":
                    raise FormulaParenthesisError(formula)

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
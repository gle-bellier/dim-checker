from typing import Tuple

from dim_checker.errors.formula_errors import FormulaCharacterError, FormulaParenthesisError 





class VectorFormula:
    
    def __init__(self, vector_formula:str) -> None:
        """Initializes vector formula object.

        Args:
            formula (str): vector formula.
        """
        self.vector_formula = vector_formula
        self.dims, self.variables = self.parse_vector_formula(vector_formula)

    def __repr__(self) -> str:
        """Creates string representation of the vector formula.

        Returns:
            str: string representation of the vector formula.
        """
        return f"""Vector formula: "{self.vector_formula}"."""

    def parse_vector_formula(self, vector_formula: str) -> Tuple[list[str], set[str]]:
        """Parse the vector formula into list of the dimensions and the set 
        of variables involved in the dimensions definitions. 

        Args:
            vector_formula (str): input or output vector formula.

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

        for c in vector_formula:
            if c == "(":
                exp += c
                n_par += 1

            elif c == ")":
                
                # raise error if empty parenthesis
                if exp == "(":
                    raise FormulaParenthesisError(vector_formula)

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
                        raise FormulaCharacterError(vector_formula, c)

        # raise error if there is unclosed parenthesis
        if n_par != 0:
            raise FormulaParenthesisError(vector_formula)


        return dims, variables




class Formula:

    def __init__(self, formula: str) -> None:
        """Initializes formula object.

        Args:
            formula (str): formula string description.
        """
        self.formula = formula
        self.vector_formulas = self.parse_formula(formula)

    def parse_formula(self, formula: str) -> list[VectorFormula]:
        """Parse formula into vector formulas.

        Args:
            formula (str): formula string description.

        Returns:
            list[VectorFormula]: list of VectorFormulas corresponding to 
            each vector formulas included in formula.
        """
        # remove spaces
        formula = formula.replace(" ", "")
        # split formula to get each vector formula
        vector_formulas = formula.split(",")
        # create vector formula for each non empty formula
        return [VectorFormula(vf) for vf in vector_formulas if vf!=""]


    def __repr__(self) -> str:
        """Creates string representation of the formula.

        Returns:
            str: string representation of the formula.
        """
        s = f"Formula composed of {len(self.vector_formulas)} vector formula(s): "
        for vf in self.vector_formulas:
            s+=f"\n -> {str(vf)}"
        return s




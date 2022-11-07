from typing import Any, List, Tuple, Dict


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

        in_dims, in_variables = self.parse_formula(in_formula)
        out_dims, out_variables = self.parse_formula(out_formula)

    def parse_pattern(pattern: str) -> Tuple[list, list]:
        """Parse the pattern and return input and output formulas included in pattern".

        Args:
            pattern (str): pattern.

        Returns:
            Tuple[list, list, set]: results of the patterns parsing, start dimensions, 
            end dimensions and variables used for dimensions definition.
        """
        # remove spaces
        pattern = pattern.replace(" ", "")
        # split the formula
        return pattern.split("->")
        

            
    def parse_pattern(pattern: str) -> Tuple[list, set]:
        """Parse the input or output dimensions pattern into list 
        of the dimensions and the set of variables involved in the 
        dimensions definitions. 

        Args:
            pattern (str): valid pattern.

        Raises:
            ValueError: error if an unauthorized caracter is used in the 
            pattern string.

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
        formula = ""

        for c in pattern:
            if c == "(":
                formula += c
                n_par += 1

            elif c == ")":
                n_par -= 1
                formula += c
                # if the formula ends add it to the dimensions, else keep going.
                if n_par == 0:
                    dims += [formula]
                    # reset formula
                    formula = ""

            else:
                if n_par > 0:
                    formula += c
                    # if the caracter is a letter, it is a dimension
                    # we need to store
                    if c.isalpha():
                        variables.add(c)
                else:
                    if c.isalpha():
                        dims += [c]
                        variables.add(c)

                    else:
                        raise ValueError(
                            f"Caracter {c} is not valid for dimensions. Must be a letter."
                        )
        return dims, variables



    def parse_constraints(constraints: dict) -> dict:
        """Parse the constraints and check there validity.

        Args:
            constraints (dict): dictionary of constraints on 
            dimensions.

        Raises:
            ValueError: error raised when the constant format is not appropriate.

        Returns:
            dict: valid constraints.
        """
        # check constraints validity
        for cons in constraints.keys():
            if len(cons) > 1 or not cons.isalpha():
                raise ValueError(
                    f"Constraints must be single letter dimensions, got {cons}={constraints[cons]}."
                )

        return constraints

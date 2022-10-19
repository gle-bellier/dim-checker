from typing import Any, List, Tuple, Dict



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

def parse_patterns(pattern: str) -> Tuple[list, list, set]:
    """Parse the input and output patterns included in the general pattern composed as 
    follow: "input_pattern -> output_pattern".

    Args:
        pattern (str): general pattern.

    Returns:
        Tuple[list, list, set]: results of the patterns parsing, start dimensions, 
        end dimensions and variables used for dimensions definition.
    """
    # remove spaces
    pattern = pattern.replace(" ", "")
    # split the shapes
    start_pattern, end_pattern = pattern.split("->")

    start_dims, start_variables = parse_pattern(start_pattern)
    end_dims, _ = parse_pattern(end_pattern)

    # join the two variables sets
    return start_dims, end_dims, start_variables

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

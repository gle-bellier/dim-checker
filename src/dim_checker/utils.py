import ast



def evaluate_formula(formula: str, variables: dict[str, int]) -> int:
    """Evaluate formula according to the predefined variables.

    Args:
        formula (str): formula.
        variables (dict[str, int]): predefined variables, e.g. {"n": 3}.

    Raises:
        ValueError: error raised if the formula is invalid.

    Returns:
        int: value of the evaluated formula.
    """
    whitelist = (
        ast.Expression,
        ast.Call,
        ast.Name,
        ast.Load,
        ast.BinOp,
        ast.UnaryOp,
        ast.operator,
        ast.unaryop,
        ast.cmpop,
        ast.Num,
    )

    tree = ast.parse(formula, mode='eval')
    valid = all(isinstance(node, whitelist) for node in ast.walk(tree))
    if valid:
        return eval(compile(tree, filename='', mode='eval'),
                    {"__builtins__": None}, variables)
    else:
        raise ValueError(f"Formula {formula} is not valid.")

from typing import Any, Tuple, List, Union
import torch
import numpy as np
import ast

InputTensor = Union[torch.Tensor, np.ndarray]

def get_eval_tensor(shape: List, eval_value: str or int,
                    eval_type: str) -> torch.Tensor:

    if eval_type not in ["torch", "numpy"]:
        raise ValueError(
            f"Evaluation type must be either torch or numpy, got {eval_type}.")

    if eval_value == "random":
        if eval_type == "torch":
            return torch.randn(shape)
        else:
            return np.random.randn(shape)

    elif eval_value == "zeros":
        if eval_type == "torch":
            return torch.zeros(shape)
        else:
            return np.zeros((shape))
    elif eval_value == "ones":
        if eval_type == "torch":
            return torch.ones(shape)
        else:
            return np.ones((shape))

    elif type(eval_value) in [int, float]:
        if eval_type == "torch":
            return eval_value * torch.ones(shape)
        else:
            return eval_value * np.ones((shape))

    else:
        raise ValueError(
            f"Error with eval_value = {eval_value}, must be either 'random', 'zeros', 'ones', or particular float."
        )


def evaluate_formula(formula: str, vars: dict) -> dict:
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
                    {"__builtins__": None}, vars)
    else:
        raise ValueError(f"Formula {formula} is not valid.")

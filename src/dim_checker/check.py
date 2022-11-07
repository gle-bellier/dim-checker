import torch
import numpy as np
from typing import Tuple, List, Any, Callable
import random


from dim_checker.parsing import parse_patterns, parse_constraints
from dim_checker.utils import evaluate_formula, get_eval_tensor, InputTensor


class DimChecker:
    """
    Tool to check a nn module/function/callable output dimensions. 
    """

    def __init__(self,
                 eval_value="random",
                 eval_type="torch",
                 max_size=100,
                 depth=1):
        """Initialize DimChecker.

        Args:
            eval_value (str, optional): callable evaluation point. Available options are "random", "ones", 
            "zeros", and float or int (in this case all elements of the input vector equal eval_value). 
            Defaults to "random".
            eval_type (str, optional): type of the input tensor. Available options are "torch", "numpy". Defaults to "torch".
            max_size (int, optional): maximum size of an input dimension. One may consider reducing this parameter when 
            using large neural networks requiring heavy computing ressources. Defaults to 100.
            depth (int, optional): Number of tests to run with differents input dimensions. Increasing the depth reduces the 
            risk of collisions but also increases the runtime. Defaults to 1.
        """
        self.eval_value = eval_value
        self.eval_type = eval_type
        self.max_size = max_size
        self.depth = depth

    def __repr__(self) -> str:
        """String representation of the DimChecker.

        Returns:
            str: representation string.
        """
        return f"DimChecker object with following attributes: {self.__dict__}"

    def __get_primes(self, n: int) -> List[int]:
        """Get n dictint prime numbers. This function takes into account the 
        max_size argument of the current DimChecker.

        Args:
            n (int): number of primes to return.

        Returns:
            List[int]: list of the n different primes all smaller than self.max_size.
        """
        l_primes = [
            5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
            71, 73, 79, 83, 89, 97
        ]
        # find the list of primes under max dim
        primes = [p for p in l_primes if p < self.max_size]
        if len(primes) < n:
            raise ValueError(
                "Not enough primes to test each dimension. Please consider increasing max_dim."
            )
        return random.sample(primes, n)

    def __get_variables_values(self, variables: set,
                               constraints: dict) -> dict:
        """Set a fixed value for each dimension. We use prime numbers > 3 to reduce the risk of 
        collisions when comparing the output shape. 

        Args:
            shape (set): list of the dimensions variables to assign.
            constraints (dict): constraints dictionnary.

        Returns:
            dict: dimensions dictionnary. A prime number is assigned to each dimension variables.
        """
        # get different primes
        primes = self.__get_primes(len(variables))
        d = dict(zip(variables, primes))
        # merge with the constraints
        return d | constraints

    def get_input(self, start_dims: List[str],
                  variables: dict) -> InputTensor:

        # compute input shape
        shape = [evaluate_formula(dim, variables) for dim in start_dims]
        return get_eval_tensor(shape, self.eval_value, self.eval_type)

    def __check_out_shape(self, out: torch.Tensor, end_dims: list,
                      variables: set) -> bool:

        # check if the shapes have the same length
        assert len(out.shape) == len(end_dims), f"The output shape does not have the expected number of dimensions. Expect {len(end_dims)} and got {len(out.shape)}."

        for dim, out_dim in zip(end_dims, out.shape):
            # the dimension is a formula
            if len(dim) > 1:
                assert evaluate_formula(dim, variables) == out_dim, f"Unexpected output shape. Issue with dimension '{dim}'."
            # the dimension is a letter
            else:
                if dim in variables:
                    # we need to check dim equality
                    assert int(variables[dim])== out_dim, f"Unexpected output shape. Issue with dimension '{dim}'."

    def test_dims(self, f: Callable, pattern: str, **constraints) -> None:
        """Test the output dimensions and raise error if the output pattern 
        does not match the output dimensions. Because of the rish of collisions this test 
        is not a proof that the output dimensions will always be correct but allow fast testing. 

        Args:
            f (Callable): function or nn module to test.
            pattern (str): pattern describing the input and expected output dimensions. It must respects 
            the following rules:
            -
            -
            -
            constraints: constraints over the dimensions used for the tests.

        """
        for _ in range(self.depth):
            self.__get_test_dims(f, pattern, constraints)

    def __get_test_dims(self, f: Callable, pattern: str,
                      constraints: dict) -> None:
        """Run a single test on the output dimensions. Raise error if the output pattern does not match
        the output dimensions.

        Args:
            f (Callable): function or nn module to test.
            pattern (str): pattern describing the input and expected output dimensions.
            constraints (dict): constraints on variables.
        """

        # parse pattern and constraints
        constraints = parse_constraints(constraints)
        start_dims, end_dims, start_variables = parse_patterns(pattern)
        # get primes for variables or apply constraints
        variables = self.__get_variables_values(start_variables, constraints)
        # get input
        x = self.get_input(start_dims, variables)
        # check output shape
        self.__check_out_shape(f(x), end_dims, variables)

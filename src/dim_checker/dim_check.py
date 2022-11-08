import torch
from typing import  List, Callable
import random

from dim_checker.errors.dimchecker_errors import OutputsNumberError
from dim_checker.objects import Pattern, Constraints, Formula
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

    def __get_variables_values(self, in_formula: Formula,
                               constraints: dict) -> dict:
        """Set a fixed value for each dimension. We use prime numbers > 3 to reduce the risk of 
        collisions when comparing the output shape. 

        Args:
            in_formula (Formula): input formula object.
            constraints (dict): constraints dictionnary.

        Returns:
            dict: dimensions dictionnary. A prime number is assigned to each dimension variables.
        """


        # merge all needed variables from the differents vector formulas.
        variables = set()
        for vf in in_formula.vector_formulas:
            variables = variables | vf.variables


        # get different primes and assign them to variables
        primes = self.__get_primes(len(variables))
        d = dict(zip(variables, primes))
        # merge with the constraints
        return d | constraints

    def __get_input(self, in_dims: List[str],
                  variables: dict) -> InputTensor:

        # compute input shape
        shape = [evaluate_formula(dim, variables) for dim in in_dims]
        return get_eval_tensor(shape, self.eval_value, self.eval_type)

    def __check_out_shape(self, out: torch.Tensor, out_dims: list,
                      variables: dict) -> None:

        # check if the shapes have the same length
        error_str = f"The output shape does not have the expected number of dimensions. Expect {len(out_dims)} and got {len(out.shape)}."
        assert len(out.shape) == len(out_dims), error_str

        for dim, out_dim in zip(out_dims, out.shape):
            # the dimension is a formula
            if len(dim) > 1:
                error_str = f"Unexpected output shape. Issue with dimension '{dim}'."
                assert evaluate_formula(dim, variables) == out_dim, error_str
            # the dimension is a letter
            else:
                if dim in variables:
                    # we need to check dim equality
                    error_str = f"Unexpected output shape. Issue with dimension '{dim}'."
                    assert int(variables[dim])== out_dim, error_str
    
    def __run_one_test(self, f: Callable, pattern: Pattern,
                      constraints: Constraints) -> None:
        """Run a single test on the output dimensions. Raise error if the output pattern does not match
        the output dimensions.

        Args:
            f (Callable): function or nn module to test.
            pattern (Pattern): pattern describing the input and expected output dimensions.
            constraints (Constraints): constraints on variables.
        """
        # get evaluation primes for variables and apply constraints
        eval_variables = self.__get_variables_values(pattern.in_formula, constraints.constraints)
        
        
        # get input vectors
        in_vectors = []
        for in_vf in pattern.in_formula.vector_formulas:
            in_vectors += [self.__get_input(in_vf.dims, eval_variables)]

        # get outputs
        outputs = f(*in_vectors)
        # if there is only one output we convert it to a tuple
        if not isinstance(outputs, tuple):
            outputs=(outputs,)

        # check if the number of outputs corresponds to the expected number.
        if len(outputs)!=len(pattern.out_formula.vector_formulas):
            raise OutputsNumberError(len(outputs), len(pattern.out_formula.vector_formulas))

        # check outputs dimensions
        for out, out_vf in zip(outputs, pattern.out_formula.vector_formulas):
            self.__check_out_shape(out, out_vf.dims, eval_variables)
            

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
        # parse pattern and constraints
        p = Pattern(pattern)
        c = Constraints(constraints)
        for _ in range(self.depth):
            self.__run_one_test(f, p, c)





def f(x, y):
    return x+y


DimChecker().test_dims(f, "bcl, bcl->bcl, bcl")
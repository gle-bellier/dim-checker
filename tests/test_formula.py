import pytest
from dim_checker.objects import VectorFormula, Formula




@pytest.mark.parametrize("formula, dims, variables"
, [
    ("bcl", ["b", "c", "l"], {"b", "c", "l"}),
    ("b(2*c+1)l", ["b", "(2*c+1)", "l"], {"b", "c", "l"}),
     
    
])
def test_vector_formula(formula: str, dims: list[str], variables: set[str]) -> None:

    vf =  VectorFormula(formula)
    assert vf.dims == dims, vf.variables == variables 



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



@pytest.mark.parametrize("formula, nb_vf"
, [
    ("bcl", 1),
    ("b(2*c+1)l", 1),
    ("bcl, bl", 2),
    ("b(2*c+1)l, bdl, dhd", 3),
     
    
])
def test_formula_vector_formulas(formula: str, nb_vf: int) -> None:

    f =  Formula(formula)
    assert len(f.vector_formulas)==nb_vf 




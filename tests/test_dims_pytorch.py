import torch
from dim_checker.check import DimChecker

import pytest


@pytest.mark.parametrize("pattern, constraints", [
    ("bcl->bcn", {
        "n": 1
    }),
    ("bcn->bcn", {
        "n": 1
    }),
    ("bclk->bcln", {
        "n": 1
    }),
])
def test_sum_last_dim(pattern: str, constraints: dict) -> None:

    def f(x):
        return torch.sum(x, dim=-1,  keepdim=True)
        
    DimChecker().test_dims(f, pattern, **constraints)


@pytest.mark.parametrize("pattern, constraints", [
    ("bcl->bcn", {
        "n": 0
    }),
    ("bcl->bcl", {"l":2}),
    ("bcl->bcnlj", {
        "n": 1
    }),
])
def test_error_sum_last_dim(pattern: str, constraints: dict) -> None:

    def f(x):
        return torch.sum(x, dim=-1,  keepdim=True)
        
    with pytest.raises(Exception) as excinfo:
        DimChecker().test_dims(f, pattern, **constraints)

    assert not "Error should have been raised." in str(excinfo.value)




@pytest.mark.parametrize("pattern, constraints", [
    ("bcl->bnl", {
        "n": 1
    }),
    ("qwecn->qwebn", {
        "b": 1
    }),
    ("b(2*c+1)l->bcl", {
        "c": 1
    }),
])
def test_sum_m2_dim(pattern: str, constraints: dict) -> None:
    def f(x):
        return torch.sum(x, dim=-2,  keepdim=True)
    DimChecker().test_dims(f, pattern, **constraints)


@pytest.mark.parametrize("pattern, constraints", [
    ("bcl->bcn", {
        "n": 0
    }),
    ("bcl->bcl", {"l":1}),
    ("bcl->bcnlj", {
        "n": 1
    }),
])
def test_error_sum_m2_dim(pattern: str, constraints: dict) -> None:

    def f(x):
        return torch.sum(x, dim=-2,  keepdim=True)
        
    with pytest.raises(Exception) as excinfo:
        DimChecker().test_dims(f, pattern, **constraints)

    assert not "Error should have been raised." in str(excinfo.value)

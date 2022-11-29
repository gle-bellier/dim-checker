import torch
from dim_checker.dim_check import DimChecker

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

@pytest.mark.parametrize("pattern, constraints", [
    ("bcl, bcl ->bcn", {
    }),
    ("bcl, bnc->bcl", {"l":1}),
    ("bcl, qwer->bcl", {
        "n": 1
    }),
])
def test_multi_input(pattern: str, constraints: dict) -> None:

    def f(x, y):
        return x
        
    DimChecker().test_dims(f, pattern, **constraints)

@pytest.mark.parametrize("pattern, constraints", [
    ("bcl, bcl->bcn", {
        "n": 0
    }),
    ("bcl, bcl->bc(2*l)", {"l":1}),
    ("bcl, bcn->bcnlj", {
        "n": 1
    }),
])
def test_error_multi_input(pattern: str, constraints: dict) -> None:

    def f(x, y):
       return x 

    with pytest.raises(Exception) as excinfo:
        DimChecker().test_dims(f, pattern, **constraints)

    assert not "Error should have been raised." in str(excinfo.value)

@pytest.mark.parametrize("pattern, constraints", [
    ("bcl->bcl, bcn", {
    }),
    ("bcl->bcl, bcn", {"n":1}),
])
def test_multi_output(pattern: str, constraints: dict) -> None:

    def f(x):
        return x, x[...,0:1]
        
    DimChecker().test_dims(f, pattern, **constraints)

@pytest.mark.parametrize("pattern, constraints", [
    ("bcl->bcn, bcm", {
        "n": 0
    }),
    ("bcl->nc, bc(2*l)", {"l":1}),
    ("bcl->bcl, bcl bcnlj", {
        "n": 1
    }),
])
def test_error_multi_output(pattern: str, constraints: dict) -> None:

    def f(x, y):
       return x 

    with pytest.raises(Exception) as excinfo:
        DimChecker().test_dims(f, pattern, **constraints)

    assert not "Error should have been raised." in str(excinfo.value)

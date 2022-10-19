import torch
from dim_checker.check import DimChecker

import pytest


@pytest.mark.parametrize("pattern, constraints", [
    ("bcl->bcn", {
        "n": 1
    }),
    ("bcl->bcn", {
        "n": 1
    }),
    ("bcl->bcn", {
        "n": 1
    }),
])
def test_sum_last_dim(pattern: str, constraints: dict) -> None:

    def f(x):
        return torch.sum(x, dim=-1,  keepdim=True)

    DimChecker().test_dims(f, pattern, **constraints)

import torch
import numpy as np


class Vector:

    def __init__(self, shape: list[int], eval_value: str or int, eval_type: str, device: str) -> None:
        self.shape = shape
        self.eval_value = eval_value
        self.eval_type = eval_type
        self.device = device
        

    @property
    def eval_vector(self) -> torch.Tensor or np.ndarray:

        if self.eval_type not in ["torch", "numpy"]:
            raise ValueError(
                f"Evaluation type must be either torch or numpy, got {self.eval_type}.")

        if self.eval_value == "random":
            if self.eval_type == "torch":
                return torch.randn(self.shape, device=self.device)
            else:
                return np.random.randn(self.shape)

        elif self.eval_value == "zeros":
            if self.eval_type == "torch":
                return torch.zeros(self.shape, device=self.device)
            else:
                return np.zeros((self.shape))
        elif self.eval_value == "ones":
            if self.eval_type == "torch":
                return torch.ones(self.shape, device=self.device)
            else:
                return np.ones((self.shape))

        elif type(self.eval_value) in [int, float]:
            if self.eval_type == "torch":
                return self.eval_value * torch.ones(self.shape, device=self.device)
            else:
                return self.eval_value * np.ones((self.shape))

        else:
            raise ValueError(
                f"Error with eval_value = {self.eval_value}, must be either 'random', 'zeros', 'ones', or particular float."
            )






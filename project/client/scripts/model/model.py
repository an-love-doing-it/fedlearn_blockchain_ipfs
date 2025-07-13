from typing import Any

import torch
import torch.nn as nn


class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28 * 28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


def get_loss_function_optimizer(model: Model) -> dict[str, Any]:
    return {
        "loss_fn": torch.nn.CrossEntropyLoss(),
        "optimizer": torch.optim.Adam(model.parameters()),
    }
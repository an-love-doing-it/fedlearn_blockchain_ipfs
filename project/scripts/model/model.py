from typing import Any

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor


class Model(nn.Module): #CNN
    def __init__(self):
        super().__init__()
        
        self.layer1 = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        
        self.layer2 = nn.Sequential(
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        
        self.fc1 = nn.Linear(in_features=64*6*6, out_features=600)
        self.drop = nn.Dropout2d(0.25)
        self.fc2 = nn.Linear(in_features=600, out_features=120)
        self.fc3 = nn.Linear(in_features=120, out_features=10)
        
    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.view(out.size(0), -1)
        out = self.fc1(out)
        out = self.drop(out)
        out = self.fc2(out)
        out = self.fc3(out)
        
        return out


def get_loss(): 
    return nn.CrossEntropyLoss()


def get_optim(model: Model, *, lr=0.001): 
    return torch.optim.Adam(model.parameters(), lr)


def get_train_data(*, batch_size: int = 64) -> DataLoader:
    training_data = datasets.FashionMNIST(
        root=".\\data", train=True, download=True, transform=ToTensor()
    )
    train_dataloader = DataLoader(
        training_data, batch_size=batch_size, shuffle=True
    )
    return train_dataloader


def get_test_data(*, batch_size: int = 64) -> DataLoader:
    test_data = datasets.FashionMNIST(
        root=".\\data", train=False, download=True, transform=ToTensor()
    )
    test_dataloader = DataLoader(
        test_data, batch_size=batch_size, shuffle=True
    )
    return test_dataloader
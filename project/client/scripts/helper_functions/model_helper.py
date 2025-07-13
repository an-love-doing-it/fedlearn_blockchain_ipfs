import os

import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
import ipfs_api

from helper_functions.solidity_helper import get_latest_weight, get_model
from model.model import (
    Model, 
    get_loss_function_optimizer as get_loss_op
)


def get_train_data(batch_size: int = 64) -> DataLoader:
    training_data = datasets.FashionMNIST(
        root=".\\data", train=True, download=True, transform=ToTensor()
    )
    train_dataloader = DataLoader(
        training_data, batch_size=batch_size, shuffle=True
    )
    return train_dataloader


def get_test_data(batch_size: int = 64) -> DataLoader:
    test_data = datasets.FashionMNIST(
        root=".\\data", train=False, download=True, transform=ToTensor()
    )
    test_dataloader = DataLoader(
        test_data, batch_size=batch_size, shuffle=True
    )
    return test_dataloader


def train(model: Model, data: DataLoader, 
        epochs: int = 5, debug: bool = False) -> None:
    model.train()
    loss_fn, optimizer = get_loss_op(model).values()
    batch_size = data.batch_size
    
    for epoch in range(epochs):
        if debug is True: print(f"Batch #{epoch + 1}")
        
        for batch, (X, y) in enumerate(data):
            pred = model(X)
            loss = loss_fn(pred, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            if debug is True:
                print(f"\rProgress: {(int)((batch+1) / batch_size):02}", end="")


def test(model: Model, data: DataLoader) -> float:
    model.eval()
    loss_fn = get_loss_op(model)["loss_fn"]
    with torch.no_grad():
        for X, y in data:
            pred = model(X)
            loss = loss_fn(pred, y) 
            correct = (pred.argmax(1) == y).sum().item()

    return correct / len(data.dataset)


def save_struct(model: Model) -> str:
    if not os.path.exists(".\\current_weight\\model.pth"):
        torch.save(model, ".\\current_weight\\model.pth")

    return ipfs_api.publish(".\\current_weight\\model.pth")


def save_weight(model) -> str:
    if not os.path.exists(".\\current_weight\\model_weight.pth"):
        torch.save(model.state_dict(), ".\\current_weight\\model_weight.pth")

    return ipfs_api.publish(".\\current_weight\\model_weight.pth")


def load_struct(contract):
    if not os.path.exists(".\\current_weight\\model.pth"):
        ipfs_api.download(get_model(contract), ".\\current_weight\\model.pth")

    model = torch.load(".\\current_weight\\model.pth", weights_only=False)
    return model


def load_weight(contract):
    model = load_struct(contract)

    ipfs_api.download(
        get_latest_weight(contract), ".\\current_weight\\model_weight.pth"
    )

    model.load_state_dict(
        torch.load(".\\current_weight\\model_weight.pth", weights_only=True)
    )
    return model


def execute_round(contract, epochs=5):
    model = load_weight(contract)
    train_data = get_train_data()
    train(model, train_data, epochs=epochs, debug=True)

    precision = test(model, get_test_data())

    print(f"ACCURACY : {precision*100:03.5f}%")

    return model, precision

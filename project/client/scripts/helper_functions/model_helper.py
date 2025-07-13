import os

import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
import ipfs_api

from helper_functions.solidity_helper import get_latest_model
from model.model import Model, get_loss, get_optim


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


def train(model: Model, device, data: DataLoader,  optimizer, *, loss_fn = get_loss(),
        epochs: int = 5, debug: bool = False) -> None:
    model.train()
    for epoch in range(epochs):
        if debug is True: 
            print(f"Epoch #{epoch + 1}")
            total = len(data.dataset)
        
        for batch, (inputs, labels) in enumerate(data):
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = loss_fn(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            if debug is True:
                print(f"\rProgress: {batch*data.batch_size + len(labels)}/{total} Loss: {loss}", end="")
        if debug is True:
            print()
            print(f"{test(model, device, get_test_data())*100}%")


def test(model: Model, device, data: DataLoader, loss_fn=get_loss()) -> float:
    model.eval()
    total = 0
    correct = 0
    with torch.no_grad():
        for inputs, labels in data:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predictions = torch.max(outputs, 1)
            correct += (predictions == labels).sum().item()
            total += len(labels)
    return correct / total


def save_checkpoint(model: Model, optimizer, filename) -> str:
    save_path = f".\\current_weight\\{filename}"
    torch.save({
        "model_state": model.state_dict(),
        "optimizer_state": optimizer.state_dict()
    }, save_path)

    return ipfs_api.publish(save_path)


def save_checkpoint(model: Model, optimizer, filename) -> str:
    save_path = f".\\current_weight\\{filename}"
    torch.save({
        "model_state": model.state_dict(),
        "optimizer_state": optimizer.state_dict()
    }, save_path)

    return ipfs_api.publish(save_path)


def load_checkpoint(contract, filename):
    load_path = f".\\current_weight\\{filename}"
    ipfs_api.download(
        get_latest_model(contract), 
        load_path
        )

    checkpoint = torch.load(load_path)
    model = Model()
    model.load_state_dict(checkpoint.get("model_state"))
    optimizer = get_optim(model)
    optimizer.load_state_dict(checkpoint["optimizer_state"])
    return model, optimizer


def load_and_train(contract, filename, device, *, epochs=5, debug=False):
    model, optimizer = load_checkpoint(contract, filename)
    train_data = get_train_data()
    train(model, device, train_data, optimizer, epochs=epochs, debug=debug)

    precision = test(model, device, get_test_data())

    print(f"ACCURACY : {precision*100:03.5f}%")

    return model, optimizer, precision

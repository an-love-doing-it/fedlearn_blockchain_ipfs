import os

import torch
from torch.utils.data import DataLoader
import ipfs_api

from helper_functions.solidity_helper import get_latest_model
from model.model import (
    Model, get_loss, get_optim, 
    get_test_data, get_train_data
    )


def train(
        model: Model, 
        train_data: DataLoader, 
        *, 
        device="cpu", 
        optimizer, 
        loss_fn=get_loss(),
        epochs: int = 5, 
        debug: bool = False
        ) -> None:
    """
    Train the model epochs time
    """
    model.train()
    for epoch in range(epochs):
        if debug is True: 
            print(f"Epoch #{epoch + 1}")
            total = len(train_data.dataset)
        
        for batch, (inputs, labels) in enumerate(train_data):
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = loss_fn(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            if debug is True:
                print(f"\rProgress: {batch*train_data.batch_size + len(labels)}/{total} Loss: {loss}", end="")
        if debug is True:
            print()
            print(f"{test(model, device, get_test_data())*100}%")


def test(
        model: Model, 
        data: DataLoader, 
        *, 
        device="cpu", 
        loss_fn=get_loss()
        ) -> float:
    """
    Test the model and return its accuracy/precision
    """
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


def save_checkpoint(
        model: Model, 
        optimizer, 
        *, 
        filename="current_checkpoint.path"
        ) -> str:   
    """
    Save the model's and optimizer's state_dict to a file,
    push it to IPFS and return its CID.
    """
    save_path = os.path.join(".", "current_weight", filename)
    torch.save({
        "model_state": model.state_dict(),
        "optimizer_state": optimizer.state_dict()
        }, save_path)
    
    return ipfs_api.publish(save_path)


def load_checkpoint(contract, *, filename="last_checkpoint.pth"):  
    """
    Save the last model uploaded to blockchain through IPFS to local end device
    """
    load_path = os.path.join(".", "current_weight", filename)
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
    """
    Load the model and optimizer from last check point and train it,
    return the new model and optimizer, the model's accuracy
    """
    model, optimizer = load_checkpoint(contract, filename)
    train_data = get_train_data()
    train(
        model, get_train_data(), device=device, optimizer=optimizer,
        epochs=epochs, debug=debug
        )
    
    precision = test(model, device, get_test_data())
    if debug is True:
        print(f"ACCURACY : {precision:03.5%}")
    
    return model, optimizer, precision

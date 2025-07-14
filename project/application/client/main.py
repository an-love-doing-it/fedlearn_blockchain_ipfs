import json

from load_dotenv import load_dotenv
from web3 import Web3, HTTPProvider
import torch

from helper_functions.solidity_helper import transact, get_latest_model
from helper_functions.model_helper import (
    save_checkpoint, load_checkpoint,
    test, get_test_data, 
    train, get_train_data,
    load_and_train
    )
from model.model import Model, get_optim, get_loss

# load environment's variable
# load_dotenv()


#--------------------------CLIENT SIDE CODE------------------------------------

device = "cuda" if torch.cuda.is_available() else "cpu"


# get contract's abi and address
with open("access.json", "r") as f:
    access = json.load(f)
    abi = access.get("abi")
    address = access.get("contractAddress")
    
# setup blockchain node endpoint
endpoint = HTTPProvider(
    "https://sepolia.infura.io/v3/68fc2f0419b146cfa20569d65672ac7f"
    )
w3_worker = Web3(endpoint)
if not w3_worker.is_connected():
    raise Exception("Web3 is not connected.")

# setup account
private_key_worker = "0x25b9b11711c396c7e81c55a2fee1577a5cdb75785f3949c9df8569cda7be1014"

# create a contract
contract_object = w3_worker.eth.contract(address=address, abi=abi)

for i in range(3):
    print(f"Round #{i+1}")
    model, optimizer, precision = load_and_train(
        contract=contract_object, 
        filename="last_model.pth", 
        device=device,
        epochs=5,
        debug=True
        )
    training = contract_object.functions.submit_model_weight(
        save_checkpoint(model, optimizer, "current_model.pth"),
        (int)(precision * 10**8)
        )
    reciept = transact(w3_worker, training, private_key_worker)
    print(reciept)
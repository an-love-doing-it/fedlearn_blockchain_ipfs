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
    "HTTP://127.0.0.1:7545"
    )
w3_worker = Web3(endpoint)
if not w3_worker.is_connected():
    raise Exception("Web3 is not connected.")

# setup account
private_key_worker = "WORKER_PRIVATE_KEY"

# create a contract
contract_object = w3_worker.eth.contract(address=address, abi=abi)

for i in range(3):
    print(f"Round #{i+1}")
    model, optimizer, precision = load_and_train(
        contract=contract_object, 
        filename="last_model.pth", 
        device=device,
        debug=True
        )
    training = contract_object.functions.submit_model_weight(
        save_checkpoint(model, optimizer, "current_model.pth"),
        (int)(precision * 10**8)
        )
    reciept = transact(w3_worker, training, private_key_worker)
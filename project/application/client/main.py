import json
import os

from load_dotenv import load_dotenv
from web3 import Web3, HTTPProvider
import torch

from scripts.helper_functions.solidity_helper import transact, get_latest_model
from scripts.helper_functions.model_helper import (
    save_checkpoint, load_checkpoint,
    test, train,
    load_and_train
    )
from scripts.model.model import Model, get_optim, get_loss
# load environment's variable
# load_dotenv()


#--------------------------CLIENT SIDE CODE------------------------------------

device = "cuda" if torch.cuda.is_available() else "cpu"


# get contract's abi and address
access_path = os.path.join("application", "client", "access.json")
with open(access_path, "r") as f:
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
private_key_worker = "0x80e4edfa096be6bfd55e3ccecc29453580b8452539a8828778b252fe2e033ef1"

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
        save_checkpoint(model, optimizer, filename="current_model.pth"),
        (int)(precision * 10**8)
        )
    reciept = transact(w3_worker, training, private_key_worker)
    print(reciept)
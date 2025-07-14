import json

from load_dotenv import load_dotenv
from web3 import Web3, HTTPProvider
import torch

from helper_functions.solidity_helper import (
    compile_sol, get_abi_bin, transact
    )
from helper_functions.model_helper import (
    save_checkpoint, test, get_test_data, train, get_train_data
    )
from model.model import Model, get_optim, get_loss

# load environment's variable
# load_dotenv()


#--------------------------SERVER SIDE CODE------------------------------------

device = "cuda" if torch.cuda.is_available() else "cpu"

# compile contract and get abi, binary code
compiled_contract = compile_sol("ModelStorage.sol", sol_ver_str="0.8.7")
abi, bin = get_abi_bin(compiled_contract)

# setup blockchain node endpoint
endpoint = HTTPProvider(
    "HTTP://127.0.0.1:7545" #Ganache
    )
w3_owner = Web3(endpoint)
if not w3_owner.is_connected():
    raise Exception("Web3 is not connected.")

# setup account
private_key_owner = "OWNER_PRIVATE_KEY"

# (setup constructor's arguments)
model = Model()
optimizer = get_optim(model)
loss_fn = get_loss()
accuracy = test(model, device, get_test_data())

# create a contract
contract_object = w3_owner.eth.contract(abi=abi, bytecode=bin)

# init the contract 
constructor = contract_object.constructor(
    save_checkpoint(model, optimizer, "current_checkpoint.pth"),
    (int)(accuracy * 10**8)
    )
receipt = transact(w3_owner, constructor, private_key_owner)
print("Constructor's reciept:\n", receipt)

# get the contract address + abi for worker
contract_address = receipt.contractAddress
contract_access = {
    "contractAddress": contract_address,
    "abi": abi,
    }

# send access to zones
with open("..\\client\\access.json", "w") as f:
    json.dump(contract_access, f)


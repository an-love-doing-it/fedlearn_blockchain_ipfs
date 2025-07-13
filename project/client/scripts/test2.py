import os

from load_dotenv import load_dotenv
from web3 import Web3, HTTPProvider

from helper_functions.solidity_helper import (
    compile_sol, get_abi_bin, transact
)
from helper_functions.model_helper import (
    save_struct, execute_round, save_weight, test, get_test_data
)
from model.model import Model

# load environment's variable
# load_dotenv()


#--------------------------SERVER SIDE CODE------------------------------------

# compile contract and get abi, binary code
compiled_contract = compile_sol("ModelStorage.sol", sol_ver_str="0.8.7")
abi, bin = get_abi_bin(compiled_contract)

# setup blockchain node endpoint
endpoint = HTTPProvider(
    "HTTP://127.0.0.1:7545"
)
w3_owner = Web3(endpoint)
if not w3_owner.is_connected():
    raise Exception("Web3 is not connected.")

# setup account
private_key_owner = "0x414c3401c88440e4a465348efc2e8a21c654cc1ea04e331c437a330b6e2aa3dd"

# (setup constructor's arguments)
model = Model()
cid_struct = save_struct(model)
cid_weight = save_weight(model)
accuracy = test(model, get_test_data())
contract_object = w3_owner.eth.contract(abi=abi, bytecode=bin)

# init the contract 
constructor = contract_object.constructor(
    cid_struct, cid_weight, f"{accuracy:03.5}"
)
receipt = transact(w3_owner, constructor, private_key_owner)
print(receipt)

# get the contract address + abi for worker
contract_address = receipt.contractAddress
contract_access = {
    "contractAddress": contract_address,
    "abi": abi,
}


#--------------------------CLIENT SIDE CODE------------------------------------
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


load_dotenv()

compiled_contract = compile_sol("ModelStorage.sol", sol_ver_str="0.8.7")
abi, bin = get_abi_bin(compiled_contract)

endpoint = HTTPProvider(
    "HTTP://127.0.0.1:7545"
)
w3 = Web3(endpoint)

if not w3.is_connected():
    raise Exception("Web3 is not connected.")


private_key = os.environ.get("PRIVATE_KEY")
account = w3.eth.account.from_key(private_key)
public_key = account.address


### init only for owner
model = Model()
cid_struct = save_struct(model)
cid_weight = save_weight(model)
accuracy = test(model, get_test_data())
contract_object = w3.eth.contract(abi=abi, bytecode=bin)
tx_hash = contract_object.constructor(
    cid_struct, cid_weight, int(accuracy * 10**8)
).transact({"from": account})
tx_reciept = w3.eth.wait_for_transaction_receipt(tx_hash)
address = w3.eth.get_transaction_receipt(w3.eth.get_block("latest")["transactions"][0])[
    "contractAddress"
]

### client side code
round = 5
for i in range(round):
    print(address)
    contract_object_client = w3.eth.contract(address=address, abi=abi)
    refined_model, precision = execute_round(contract_object_client, 1)
    transact(
        w3,
        contract_object_client.functions.submit_model_weight(
            save_weight(refined_model), int(precision * 10**8)
        ),
        account,
    )

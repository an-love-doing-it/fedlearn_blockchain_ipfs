import os
import json

from solcx import (
    compile_files, 
    install_solc, 
    get_installed_solc_versions
)
from web3 import Web3


def compile_sol(filename: str, sol_ver_str: str) -> str:
    install_solc(sol_ver_str)
    
    sol_file_path = f"solidity_files\\{filename}"
    compiled_contract = compile_files(
        source_files=sol_file_path,
        output_values=["abi", "bin"],
        solc_version=sol_ver_str,
    )
    compiled_file_name = f"{os.path.splitext(filename)[0]}.json"

    with open(f"solidity_files\\{compiled_file_name}", "w") as f:
        json.dump(compiled_contract, f)

    return compiled_file_name


def get_abi_bin(filename: str):
    with open(f".\\solidity_files\\{filename}", "r") as f:
        compiled = list(json.load(f).values())[0]
        abi, bin = compiled.get("abi"), compiled.get("bin")
    return abi, bin


def transact(w3: Web3, function_call, private_key):
    public_key = w3.eth.account.from_key(private_key).address
    transaction = function_call.build_transaction({
        'from': public_key,
        'nonce': w3.eth.get_transaction_count(public_key),
    })
    signed_transaction = w3.eth.account.sign_transaction(
        transaction, private_key=private_key
    )
    tx_hash = w3.eth.send_raw_transaction(signed_transaction.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt


def get_latest_model(contract):
    return contract.functions.get_latest_model_ipfs().call()


# def get_loss_fn(contract):
#     return contract.functions.get_loss_function().call()


# def get_optimizer(contract):
#     return contract.functions.get_optimizer().call()

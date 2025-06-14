from solcx import compile_files, install_solc, get_installed_solc_versions
import os, json
from web3 import Web3


def compile_sol(filename: str, sol_ver_str: str = None) -> str:
    """
    compile solidity file given the compiler version(opt)

    if the version input is None then use the latest compiler version
    once done compiling, write the result into a same-name json file in the same folder
    """

    install_solc(sol_ver_str or "latest")

    # ? getting the file's absolute path

    sol_file_path = os.path.join(".\\solidity_files", filename)

    compiled_contract = compile_files(
        source_files=sol_file_path,
        output_values=["abi", "bin"],
        solc_version=sol_ver_str or get_installed_solc_versions()[0],
    )
    compile_name = f"{os.path.splitext(filename)[0]}.json"

    with open(os.path.join(".\\solidity_files", compile_name), "w") as f:
        json.dump(compiled_contract, f)

    return compile_name


def get_abi_bin(filename: str):
    """
    get the ABI and bytecode (respectively)
    """

    with open(os.path.join(".\\solidity_files", filename), "r") as f:
        compiled = list(json.load(f).values())[0]
        abi, bin = compiled.get("abi"), compiled.get("bin")
    return abi, bin


def transact(web3Provider: Web3, change, fromAccount):
    """
    a compound function for transacts on the blockchain

    returns the transaction's reciept
    """
    tx_hash = change.transact({"from": fromAccount})
    return web3Provider.eth.wait_for_transaction_receipt(tx_hash)


def get_latest_weight(contract):
    return contract.functions.get_latest_model_weight().call()


def get_model(contract):
    return contract.functions.get_model().call()

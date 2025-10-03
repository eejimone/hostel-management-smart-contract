from brownie import accounts, SimpleStorage


def deploy():
    """Deploy the SimpleStorage contract."""
    # Get the account to deploy from
    account = accounts[0]
    print(f"Deploying from account: {account}")
    
    # Deploy the contract
    simple_storage = SimpleStorage.deploy({"from": account})
    print(f"Contract deployed at: {simple_storage.address}")
    
    # Interact with the deployed contract
    print(f"Initial value: {simple_storage.retrieve()}")
    
    # Store a value
    tx = simple_storage.store(42, {"from": account})
    tx.wait(1)  # Wait for 1 confirmation
    print(f"Stored value: {simple_storage.retrieve()}")

    tx = simple_storage.store(100, {"from": account})
    tx.wait(1)  # Wait for 1 confirmation
    print(f"Stored value: {simple_storage.retrieve()}")
    print(f"All stored values: {simple_storage.retrieveAll()}")

    # get contract ABI
    contract_factory = SimpleStorage
    print(f"Contract factory: {contract_factory}")
    contract_abi = simple_storage.abi
    print(f"Contract ABI: {contract_abi}")
    print(f"Contract bytecode: {contract_factory.bytecode}")
    
    # Return the deployed contract
    return simple_storage


def main():
    deploy()
from brownie import Classroom, accounts, network, web3


def get_account():
    """Return a deployer account, including for Ganache GUI RPC."""
    if len(accounts) > 0:
        return accounts[0]

    active = network.show_active()
    if active == "ganache":
        unlocked = web3.eth.accounts
        if not unlocked:
            raise ValueError("No unlocked accounts available on ganache_ui")
        return accounts.at(unlocked[0], force=True)

    raise ValueError(f"No default account configured for network '{active}'")


def deploy():
    deployer = get_account()
    contract = Classroom.deploy({"from": deployer})
    print(f"Contract deployed at: {contract.address}")
    return contract


def main():
    deploy()
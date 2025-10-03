from brownie import SimpleStorage, accounts


def test_check_favorite_number():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    
    # Act
    simple_storage.store(15, {"from": account})
    
    # Assert
    assert simple_storage.retrieve() == 15


def test_initial_value():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    
    # Assert
    assert simple_storage.retrieve() == 0
from brownie import SimpleStorage, accounts

print("first test")
def test_check_favorite_number():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    
    # Act
    simple_storage.store(15, {"from": account})
    
    # Assert
    assert simple_storage.retrieve() == 15

print
def test_initial_value():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    
    # Assert
    assert simple_storage.retrieve() == 0
print("third test")
def test_update_favorite_number():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    simple_storage.store(15, {"from": account})
    assert simple_storage.retrieve() == 15

print("fourth test")
def test_add_favorite_number():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    simple_storage.store(15, {"from": account})
    assert simple_storage.retrieve() == 15

print("fifth test")
def test_get_all_favorite_numbers():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    simple_storage.retrieveAll({"from": account})
    assert simple_storage.retrieveAll() == []


def test_get_favorite_number_by_index():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    simple_storage.store(15, {"from": account})
    assert simple_storage.retrieve()

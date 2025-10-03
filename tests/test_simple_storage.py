import pytest
from brownie import SimpleStorage, accounts


@pytest.fixture
def simple_storage():
    """Deploy a fresh SimpleStorage contract for each test."""
    account = accounts[0]
    contract = SimpleStorage.deploy({"from": account})
    return contract


@pytest.fixture
def account():
    """Provide the first account for testing."""
    return accounts[0]


def test_initial_favorite_number_is_zero(simple_storage):
    """Test that the initial favorite number is 0."""
    assert simple_storage.retrieve() == 0


def test_initial_favorite_numbers_array_is_empty(simple_storage):
    """Test that the favorite numbers array starts empty."""
    assert simple_storage.retrieveAll() == []


def test_store_single_favorite_number(simple_storage, account):
    """Test storing a single favorite number."""
    # Act
    simple_storage.store(42, {"from": account})
    
    # Assert
    assert simple_storage.retrieve() == 42
    assert simple_storage.retrieveAll() == [42]


def test_store_multiple_favorite_numbers(simple_storage, account):
    """Test storing multiple favorite numbers."""
    # Arrange
    numbers = [10, 20, 30, 40, 50]
    
    # Act
    for number in numbers:
        simple_storage.store(number, {"from": account})
    
    # Assert - retrieve() returns the last stored number
    assert simple_storage.retrieve() == 50
    # Assert - retrieveAll() returns all stored numbers
    assert simple_storage.retrieveAll() == numbers


def test_update_favorite_number(simple_storage, account):
    """Test that storing a new number updates the current favorite."""
    # Arrange - store initial value
    simple_storage.store(15, {"from": account})
    assert simple_storage.retrieve() == 15
    
    # Act - update to new value
    simple_storage.store(99, {"from": account})
    
    # Assert - current favorite is updated
    assert simple_storage.retrieve() == 99
    # Assert - both numbers are in the array
    assert simple_storage.retrieveAll() == [15, 99]


def test_store_zero(simple_storage, account):
    """Test storing zero as a favorite number."""
    # Act
    simple_storage.store(0, {"from": account})
    
    # Assert
    assert simple_storage.retrieve() == 0
    assert simple_storage.retrieveAll() == [0]


def test_store_large_number(simple_storage, account):
    """Test storing a very large number."""
    # Arrange
    large_number = 2**256 - 1  # Maximum uint256 value
    
    # Act
    simple_storage.store(large_number, {"from": account})
    
    # Assert
    assert simple_storage.retrieve() == large_number
    assert simple_storage.retrieveAll() == [large_number]


def test_store_same_number_multiple_times(simple_storage, account):
    """Test storing the same number multiple times."""
    # Act
    for _ in range(3):
        simple_storage.store(7, {"from": account})
    
    # Assert
    assert simple_storage.retrieve() == 7
    assert simple_storage.retrieveAll() == [7, 7, 7]


def test_array_preserves_order(simple_storage, account):
    """Test that the array preserves the order of stored numbers."""
    # Arrange
    numbers = [100, 50, 200, 25, 150]
    
    # Act
    for number in numbers:
        simple_storage.store(number, {"from": account})
    
    # Assert
    assert simple_storage.retrieveAll() == numbers

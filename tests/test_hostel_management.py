from brownie import HostelManagement, accounts
import pytest


@pytest.fixture
def hostel_contract():
    """Deploy a fresh HostelManagement contract for each test."""
    account = accounts[0]
    contract = HostelManagement.deploy(
        "University of Lagos",  # schoolName
        "Moremi Hall",          # hostelName
        "UNILAG Campus",        # location
        "Mr. Johnson",          # hostelManager
        100,                    # totalRooms
        50000,                  # roomPricePerMonth (in wei or smallest unit)
        {"from": account}
    )
    return contract


@pytest.fixture
def account():
    """Provide the first account for testing."""
    return accounts[0]


def test_student_registration(hostel_contract, account):
    """Test student registration and room booking."""
    # Act
    tx = hostel_contract.registerStudent(
        "Banx",
        20,
        "Male",
        "09012345678",
        "123 Main St, City",
        {"from": account}
    )
    
    # Assert
    student_details = hostel_contract.getStudentDetails()
    assert student_details[0] == "Banx"
    assert student_details[1] == 20
    assert student_details[2] == "Male"
    assert student_details[3] == "09012345678"
    assert student_details[4] == "123 Main St, City"
    assert hostel_contract.roomBooked() == True
    assert hostel_contract.occupiedRooms() == 1
    assert hostel_contract.availableRooms() == 99
    print("Student registered successfully")


def test_initial_hostel_details(hostel_contract):
    """Test that hostel details are set correctly on deployment."""
    assert hostel_contract.schoolName() == "University of Lagos"
    assert hostel_contract.hostelName() == "Moremi Hall"
    assert hostel_contract.location() == "UNILAG Campus"
    assert hostel_contract.hostelManager() == "Mr. Johnson"
    assert hostel_contract.totalRooms() == 100
    assert hostel_contract.roomPricePerMonth() == 50000
    assert hostel_contract.availableRooms() == 100
    assert hostel_contract.occupiedRooms() == 0


def test_check_availability(hostel_contract):
    """Test checking room availability."""
    availability = hostel_contract.checkAvailability()
    assert availability == 100


def test_vacate_room(hostel_contract, account):
    """Test vacating a room after booking."""
    # Arrange - Register student first
    hostel_contract.registerStudent(
        "John Doe",
        22,
        "Male",
        "08012345678",
        "456 Oak Ave",
        {"from": account}
    )
    assert hostel_contract.occupiedRooms() == 1
    
    # Act - Vacate the room
    tx = hostel_contract.vacateRoom({"from": account})
    
    # Assert
    assert hostel_contract.occupiedRooms() == 0
    assert hostel_contract.availableRooms() == 100
    assert hostel_contract.isRoomBooked() == False


def test_update_student_details(hostel_contract, account):
    """Test updating student details."""
    # Arrange - Register student first
    hostel_contract.registerStudent(
        "Jane Doe",
        21,
        "Female",
        "08123456789",
        "789 Pine St",
        {"from": account}
    )
    
    # Act - Update details
    hostel_contract.updateStudentDetails(
        "Jane Smith",
        22,
        "Female",
        "08198765432",
        "321 Elm St",
        {"from": account}
    )
    
    # Assert
    student_details = hostel_contract.getStudentDetails()
    assert student_details[0] == "Jane Smith"
    assert student_details[1] == 22
    assert student_details[3] == "08198765432"
    assert student_details[4] == "321 Elm St"


def test_update_hostel_details(hostel_contract, account):
    """Test updating hostel details."""
    # Act
    hostel_contract.updateHostelDetails(
        "University of Ibadan",
        "Queen Elizabeth Hall",
        "UI Campus",
        "Mrs. Williams",
        150,
        75000,
        {"from": account}
    )
    
    # Assert
    assert hostel_contract.schoolName() == "University of Ibadan"
    assert hostel_contract.hostelName() == "Queen Elizabeth Hall"
    assert hostel_contract.location() == "UI Campus"
    assert hostel_contract.hostelManager() == "Mrs. Williams"
    assert hostel_contract.totalRooms() == 150
    assert hostel_contract.roomPricePerMonth() == 75000


def test_room_status(hostel_contract, account):
    """Test room status changes."""
    # Check initial status
    assert hostel_contract.getRoomStatus() == "Available"
    
    # Register student
    hostel_contract.registerStudent(
        "Test Student",
        20,
        "Male",
        "08011111111",
        "Test Address",
        {"from": account}
    )
    
    # Check occupied status
    assert hostel_contract.getRoomStatus() == "Occupied"


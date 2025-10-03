from brownie import HostelManagement, accounts


def deploy_hostel(school_name, hostel_name, location, hostel_manager, total_rooms, room_price, account):
    """Deploy a new hostel management contract."""
    contract = HostelManagement.deploy(
        school_name,
        hostel_name,
        location,
        hostel_manager,
        total_rooms,
        room_price,
        {"from": account}
    )
    print(f"Contract deployed at: {contract.address}")
    return contract


def register_student(student_name, age, gender, phone_number, address, account, contract_address=None):
    """Register a student to an existing hostel contract."""
    
    # If contract address is provided, use existing contract
    if contract_address:
        contract = HostelManagement.at(contract_address)
        print(f"Using existing contract at: {contract.address}")
    else:
        raise ValueError("Contract address is required. Please deploy a hostel contract first using deploy_hostel()")
    
    # Register the student
    print(f"\nRegistering student: {student_name}")
    tx = contract.registerStudent(
        student_name,
        age,
        gender,
        phone_number,
        address,
        {"from": account}
    )
    tx.wait(1)
    
    # Verify registration
    student_details = contract.getStudentDetails()
    print(f"\n\n\n\n\n✅ Student registered successfully!")
    print(f"Name: {student_details[0]}")
    print(f"Age: {student_details[1]}")
    print(f"Gender: {student_details[2]}")
    print(f"Contact: {student_details[3]}")
    print(f"Address: {student_details[4]}")
    print(f"\nRoom Status: {contract.getRoomStatus()}")
    print(f"Available Rooms: {contract.availableRooms()}")
    print(f"Occupied Rooms: {contract.occupiedRooms()}")
    
    return contract


def vacate_room(contract, student_name, account):
    """Vacate a room"""
    print("\n\n\n\nvacating room for student:", student_name)
    tx = contract.vacateRoom({"from": account})
    tx.wait(1)
    print(f"\n\n\n\nRoom vacated for student: {student_name}")



def get_student_details(contract):
    """Retrieve student details from the contract."""
    print("\n\n\n\nFetching student details...")
    details = contract.getStudentDetails()
    if details[0] == "":
        print("No student is currently registered.")
    else:
        print(f"Student Details:\nName: {details[0]}\nAge: {details[1]}\nGender: {details[2]}\nContact: {details[3]}\nAddress: {details[4]}")
    return details



def make_payment(contract, amount, account):
    """Make a payment for room rent."""
    print(f"\n\n\n\nMaking payment of {amount}...")
    tx = contract.makePayment({"from": account, "value": amount})
    tx.wait(1)
    print(f"Payment of {amount} made successfully.")
    return tx



def main():
    # Deploy the hostel contract
    contract = deploy_hostel(
        school_name="University of Lagos",
        hostel_name="Moremi Hall",
        location="UNILAG Campus",
        hostel_manager="Mr. Johnson",
        total_rooms=100,
        room_price=50000,
        account=accounts[0]
    )
    
    # Register a student
    register_student(
        student_name="Banx",
        age=20,
        gender="Male",
        phone_number="1234567890",
        address="123 Main St",
        account=accounts[0],
        contract_address=contract.address
    )

    # Get student details
    get_student_details(contract)

    # Make payment (must be done BEFORE vacating)
    make_payment(
        contract=contract,
        amount=50000,
        account=accounts[0]
    )

    # Vacate the room (should be done AFTER payment)
    vacate_room(
        contract=contract,
        student_name="Banx",
        account=accounts[0]
    )

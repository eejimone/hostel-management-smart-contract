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


def register_students(contract, students_data):
    """Register multiple students to the contract."""
    deployer = get_account()
    for student in students_data:
        name, emailId, age, usn, department, subjects, teacherName = student
        contract.addStudentToList(
            name, emailId, age, usn, department, subjects, teacherName, 
            {"from": deployer}
        )
        print(f"Added student: {name} ({usn})")
    
    print(f"Total students registered: {contract.getStudentCount()}")


def register_single_student(contract, name, emailId, age, usn, department, subjects, teacherName):
    """Register a single student using registerStudent (for the main student slot)."""
    deployer = get_account()
    contract.registerStudent(
        name, emailId, age, usn, department, subjects, teacherName,
        {"from": deployer}
    )
    print(f"Registered main student: {name} ({usn})")


def update_student_details(contract, new_name, new_age, new_email):
    """Update the main student's details (name, age, emailId)."""
    deployer = get_account()
    contract.updateStudentDetails(new_name, new_age, new_email, {"from": deployer})
    print(f"Updated student details: {new_name}, Age: {new_age}, Email: {new_email}")




def suspend_student(contract, name, reason, duration):
    """Suspend a student by their name."""
    deployer = get_account()
    contract.suspendStudent(name, reason, duration, {"from": deployer})
    print(f"Suspended student: {name} for {duration} days due to {reason}")
    return f"Suspended student{name} for {duration} because of {reason}"


def register_teacher(contract, name, emailId, age, department, subjects):
    """Register a teacher to the contract."""
    deployer = get_account()
    contract.registerTeacher(name, emailId, age, department, subjects, {"from": deployer})
    print(f"Registered teacher: {name} ({emailId})")
    return f"Registered teacher {name} with email {emailId}"


def update_teacher_details(contract, name, new_age, new_email):
    """Update a teacher's details (age, emailId) by their name."""
    deployer = get_account()
    contract.updateTeacherDetails(name, new_age, new_email, {"from": deployer})
    print(f"Updated teacher details: {name}, Age: {new_age}, Email: {new_email}")
    return f"Updated teacher {name} details to Age: {new_age}, Email: {new_email}"

def main():
    contract = deploy()
    
    # Register a main student first
    register_single_student(
        contract, "Alice", "alice@example.com", 20, "USN001", 
        "CS", ["Math", "Science"], "Prof. Smith"
    )
    
    # Add more students to the list
    students_data = [
        ("Bob", "bob@example.com", 21, "USN002", "CS", ["Math", "English"], "Prof. Johnson"),
        ("Charlie", "charlie@example.com", 22, "USN003", "CS", ["Science", "English"], "Prof. Lee"),
    ]
    
    register_students(contract, students_data)

    # Update the main student's details
    update_student_details(contract, "Alice Updated", 21, "evidence@gmail.com")
    # Suspend a student
    suspend_student(contract, "Alice Updated", "Cheating", 7)  # Suspend Alice for 7 days due to cheating

    # Register a teacher
    register_teacher(contract, "Prof. Mahesh", "maheshtr@jainuniversity.ac.in", 45, "CS", ["Math", "Physics"])
    # Update the teacher's details
    update_teacher_details(contract, "Prof. Mahesh", 46, "maheshtr@jainuniversity.ac.in")
from brownie import Classroom, accounts, network
import pytest

@pytest.fixture
def classroom_contract():
    """Deploy a fresh Classroom contract for each test."""
    account = accounts[0]
    contract = Classroom.deploy({'from': account})
    return contract


# ============ Student Tests ============

def test_register_student(classroom_contract):
    """Test student registration."""
    contract = classroom_contract
    contract.registerStudent(
        "Banx",
        "banx@gmail.com",
        20,
        "USN001",
        "Computer Science",
        ["Math", "Physics", "Programming"],
        "Prof. Smith",
        {'from': accounts[0]}
    )
    student_details = contract.getStudentDetails()
    assert student_details[0] == "Banx"
    assert student_details[1] == 20
    assert student_details[2] == "USN001"
    assert student_details[3] == "Computer Science"
    assert student_details[4] == "Prof. Smith"


def test_update_student_details(classroom_contract):
    """Test updating student details."""
    contract = classroom_contract
    contract.registerStudent(
        "Banx", "banx@gmail.com", 20, "USN001", "Computer Science",
        ["Math", "Physics", "Programming"], "Prof. Smith"
    )
    contract.updateStudentDetails("Banx Updated", 21, "banx_updated@gmail.com", {'from': accounts[0]})
    updated_details = contract.getStudentDetails()
    assert updated_details[0] == "Banx Updated"
    assert updated_details[1] == 21


def test_suspend_student(classroom_contract):
    """Test student suspension."""
    contract = classroom_contract
    contract.registerStudent(
        "Banx", "banx@gmail.com", 20, "USN001", "Computer Science",
        ["Math", "Physics", "Programming"], "Prof. Smith", {'from': accounts[0]}
    )
    contract.suspendStudent("Banx", "Misbehavior", 86400, {'from': accounts[0]})
    assert contract.isStudentSuspended() == True


def test_get_suspension_details(classroom_contract):
    """Test getting suspension details."""
    contract = classroom_contract
    contract.registerStudent(
        "Banx", "banx@gmail.com", 20, "USN001", "Computer Science",
        ["Math", "Physics", "Programming"], "Prof. Smith", {'from': accounts[0]}
    )
    contract.suspendStudent("Banx", "Misbehavior", 86400, {'from': accounts[0]})
    suspension_details = contract.getSuspensionDetails()
    assert suspension_details[0] == "Misbehavior"
    assert suspension_details[2] == 86400


def test_get_student_subjects(classroom_contract):
    """Test getting student subjects."""
    contract = classroom_contract
    subjects = ["Math", "Physics", "Programming"]
    contract.registerStudent(
        "Banx", "banx@gmail.com", 20, "USN001", "Computer Science",
        subjects, "Prof. Smith", {'from': accounts[0]}
    )
    student_subjects = contract.getStudentSubjects()
    assert len(student_subjects) == 3
    assert "Math" in student_subjects
    assert "Physics" in student_subjects
    assert "Programming" in student_subjects


def test_add_student_to_list(classroom_contract):
    """Test adding students to the list."""
    contract = classroom_contract
    contract.addStudentToList(
        "Student1", "s1@email.com", 20, "USN001", "CS",
        ["Math"], "Prof. Smith", {'from': accounts[0]}
    )
    contract.addStudentToList(
        "Student2", "s2@email.com", 21, "USN002", "CS",
        ["Physics"], "Prof. Smith", {'from': accounts[0]}
    )
    assert contract.getStudentCount() == 2


def test_clear_student_list(classroom_contract):
    """Test clearing student list."""
    contract = classroom_contract
    contract.addStudentToList(
        "Student1", "s1@email.com", 20, "USN001", "CS",
        ["Math"], "Prof. Smith", {'from': accounts[0]}
    )
    contract.clearStudentList({'from': accounts[0]})
    assert contract.getStudentCount() == 0


# ============ Teacher Tests ============

def test_register_teacher(classroom_contract):
    """Test teacher registration."""
    contract = classroom_contract
    contract.registerTeacher(
        "Prof. Smith", "prof.smith@gmail.com", 40, "Computer Science",
        ["Math", "Physics", "Programming"], {'from': accounts[0]}
    )
    teacher_details = contract.getTeacherDetails()
    assert teacher_details[0] == "Prof. Smith"
    assert teacher_details[1] == 40
    assert teacher_details[2] == "prof.smith@gmail.com"
    assert teacher_details[3] == "Computer Science"


def test_update_teacher_details(classroom_contract):
    """Test updating teacher details."""
    contract = classroom_contract
    contract.registerTeacher(
        "Prof. Smith", "prof.smith@gmail.com", 40, "CS",
        ["Math"], {'from': accounts[0]}
    )
    contract.updateTeacherDetails("Prof. Smith Updated", 41, "updated@gmail.com", {'from': accounts[0]})
    updated_details = contract.getTeacherDetails()
    assert updated_details[0] == "Prof. Smith Updated"
    assert updated_details[1] == 41
    assert updated_details[2] == "updated@gmail.com"


def test_hire_teacher(classroom_contract):
    """Test hiring a teacher (when no teacher exists)."""
    contract = classroom_contract
    contract.hireTeacher(
        "Prof. New", "new@email.com", 35, "Mathematics",
        ["Calculus", "Algebra"], {'from': accounts[0]}
    )
    teacher_details = contract.getTeacherDetails()
    assert teacher_details[0] == "Prof. New"


def test_suspend_teacher(classroom_contract):
    """Test teacher suspension."""
    contract = classroom_contract
    contract.registerTeacher(
        "Prof. Smith", "prof@email.com", 40, "CS",
        ["Math"], {'from': accounts[0]}
    )
    contract.suspendTeacher("Prof. Smith", {'from': accounts[0]})
    assert contract.isTeacherSuspended() == True


def test_reinstate_teacher(classroom_contract):
    """Test reinstating a suspended teacher."""
    contract = classroom_contract
    contract.registerTeacher(
        "Prof. Smith", "prof@email.com", 40, "CS",
        ["Math"], {'from': accounts[0]}
    )
    contract.suspendTeacher("Prof. Smith", {'from': accounts[0]})
    assert contract.isTeacherSuspended() == True
    contract.reinstateTeacher("Prof. Smith", {'from': accounts[0]})
    assert contract.isTeacherSuspended() == False


def test_sack_teacher(classroom_contract):
    """Test sacking a teacher."""
    contract = classroom_contract
    contract.registerTeacher(
        "Prof. Smith", "prof@email.com", 40, "CS",
        ["Math"], {'from': accounts[0]}
    )
    contract.sackTeacher("Prof. Smith", {'from': accounts[0]})
    # After sacking, teacher.isHired should be False (deleted)
    # Trying to get details should fail
    with pytest.raises(Exception):
        contract.getTeacherDetails()


def test_get_teacher_subjects(classroom_contract):
    """Test getting teacher subjects."""
    contract = classroom_contract
    subjects = ["Math", "Physics", "Chemistry"]
    contract.registerTeacher(
        "Prof. Smith", "prof@email.com", 40, "CS",
        subjects, {'from': accounts[0]}
    )
    teacher_subjects = contract.getTeacherSubjects()
    assert len(teacher_subjects) == 3
    assert "Math" in teacher_subjects


def test_add_teacher_to_list(classroom_contract):
    """Test adding teachers to the list."""
    contract = classroom_contract
    contract.addTeacherToList(
        "Teacher1", "t1@email.com", 35, "CS",
        ["Math"], {'from': accounts[0]}
    )
    contract.addTeacherToList(
        "Teacher2", "t2@email.com", 40, "Physics",
        ["Physics"], {'from': accounts[0]}
    )
    assert contract.getTeacherCount() == 2


def test_clear_teacher_list(classroom_contract):
    """Test clearing teacher list."""
    contract = classroom_contract
    contract.addTeacherToList(
        "Teacher1", "t1@email.com", 35, "CS",
        ["Math"], {'from': accounts[0]}
    )
    contract.clearTeacherList({'from': accounts[0]})
    assert contract.getTeacherCount() == 0


# ============ Department Tests ============

def test_register_department(classroom_contract):
    """Test department registration."""
    contract = classroom_contract
    contract.registerDepartment(
        "Computer Science", "Dr. Ada Lovelace", 200, 20,
        ["Math", "Physics", "Programming"], [], [], {'from': accounts[0]}
    )
    dept_details = contract.getDepartmentDetails()
    assert dept_details[0] == "Computer Science"
    assert dept_details[1] == "Dr. Ada Lovelace"
    assert dept_details[2] == 200
    assert dept_details[3] == 20


def test_update_department_details(classroom_contract):
    """Test updating department details."""
    contract = classroom_contract
    contract.registerDepartment(
        "Computer Science", "Dr. Ada", 200, 20,
        ["Math"], [], [], {'from': accounts[0]}
    )
    contract.updateDepartmentDetails(
        "Computer Engineering", "Dr. Alan", 250, 25,
        [], [], {'from': accounts[0]}
    )
    updated_details = contract.getDepartmentDetails()
    assert updated_details[0] == "Computer Engineering"
    assert updated_details[1] == "Dr. Alan"
    assert updated_details[2] == 250
    assert updated_details[3] == 25


def test_deactivate_department(classroom_contract):
    """Test deactivating a department."""
    contract = classroom_contract
    contract.registerDepartment(
        "CS", "Dr. Ada", 200, 20, ["Math"], [], [], {'from': accounts[0]}
    )
    assert contract.isDepartmentActive() == True
    contract.deactivateDepartment({'from': accounts[0]})
    assert contract.isDepartmentActive() == False


def test_get_department_subjects(classroom_contract):
    """Test getting department subjects."""
    contract = classroom_contract
    subjects = ["Math", "Physics", "Chemistry", "Biology"]
    contract.registerDepartment(
        "Science", "Dr. Ada", 200, 20, subjects, [], [], {'from': accounts[0]}
    )
    dept_subjects = contract.getDepartmentSubjects()
    assert len(dept_subjects) == 4
    assert "Math" in dept_subjects
    assert "Biology" in dept_subjects


def test_get_department_count(classroom_contract):
    """Test getting department count."""
    contract = classroom_contract
    # Should always return 1 as per contract design
    assert contract.getDepartmentCount() == 1







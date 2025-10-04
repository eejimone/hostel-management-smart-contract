// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Classroom {
    address public owner;
    struct Student {
        string name;
        string emailId;
        uint256 age;
        string usn;
        string department;
        string[] subjects;
        bool isEnrolled;
        string teacherName;
        string suspensionReason;
        uint256 suspensionTimestamp;
        uint256 suspensionDuration;
    }
    Student public student;
    Student[] public students;

    struct Teacher {
        string name;
        string emailId;
        uint256 age;
        string department;
        string[] subjects;
        bool isHired;
    }
    Teacher public teacher;
    Teacher[] public teachers;


    struct Department {
        string name;
        string hodName;
        uint256 numberOfStudents;
        uint256 numberOfTeachers;
        string[] subjectsOffered;
        bool isActive;
        Student[] students;
        Teacher[] teachers;
    }
    Department public department;



    function registerStudent(string memory _name, string memory _emailId, uint256 _age, string memory _usn, string memory _department, string[] memory _subjects, string memory _teacherName) public {
        require(!student.isEnrolled, "A student is already registered.");
        student = Student({
            name: _name,
            emailId: _emailId,
            age: _age,
            usn: _usn,
            department: _department,
            subjects: _subjects,
            isEnrolled: true,
            teacherName: _teacherName,
            suspensionReason: "",
            suspensionTimestamp: 0,
            suspensionDuration: 0
        });
    }



    function getStudentDetails() public view returns (string memory, uint256, string memory, string memory, string memory) {
        require(student.isEnrolled, "No student is currently registered.");
        return (student.name, student.age, student.usn, student.department, student.teacherName);
    }


    function updateStudentDetails(string memory _name, uint256 _age, string memory _emailId) public {
        require(student.isEnrolled, "No student is currently registered.");
        student.name = _name;
        student.age = _age;
        student.emailId = _emailId;
    }
    function suspendStudent(string memory _name, string memory _reason, uint256 suspensionDuration) public {
        require(msg.sender == owner, "Only the contract owner can suspend a student.");
        require(student.isEnrolled, "No student is currently registered.");
        require(keccak256(abi.encodePacked(student.name)) == keccak256(abi.encodePacked(_name)), "Student name does not match the registered student.");
        require(suspensionDuration > 0, "Suspension time must be greater than zero.");
        require(bytes(_reason).length > 0, "Suspension reason must be provided.");
        student.isEnrolled = false;
        student.suspensionReason = _reason;
        student.suspensionTimestamp = block.timestamp;
        student.suspensionDuration = suspensionDuration;

        // the suspension will last for the specified duration
        if (block.timestamp >= student.suspensionTimestamp + student.suspensionDuration) {
            student.isEnrolled = true;
            student.suspensionReason = "";
            student.suspensionTimestamp = 0;
            student.suspensionDuration = 0;
        }
    }
    function isStudentSuspended() public view returns (bool) {
        if (!student.isEnrolled && block.timestamp < student.suspensionTimestamp + student.suspensionDuration) {
            return true;
        }
        return false;
    }

    constructor() {
        owner = msg.sender;
    }
    function registerTeacher(string memory _name, string memory _emailId, uint256 _age, string memory _department, string[] memory _subjects) public {
        require(!teacher.isHired, "A teacher is already registered.");
        teacher = Teacher({
            name: _name,
            emailId: _emailId,
            age: _age,
            department: _department,
            subjects: _subjects,
            isHired: true
        });
    }

    function getTeacherDetails() public view returns (string memory, uint256, string memory, string memory) {
        require(teacher.isHired, "No teacher is currently registered.");
        return (teacher.name, teacher.age, teacher.emailId, teacher.department);
    }
    function updateTeacherDetails(string memory _name, uint256 _age, string memory _emailId) public {
        require(teacher.isHired, "No teacher is currently registered.");
        teacher.name = _name;
        teacher.age = _age;
        teacher.emailId = _emailId;
    }
    function hireTeacher(string memory _name, string memory _emailId, uint256 _age, string memory _department, string[] memory _subjects) public {
        require(msg.sender == owner, "Only the contract owner can hire a teacher.");
        require(!teacher.isHired, "A teacher is already registered.");
        teacher = Teacher({
            name: _name,
            emailId: _emailId,
            age: _age,
            department: _department,
            subjects: _subjects,
            isHired: true
        });
    }


    function registerDepartment(string memory _name, string memory _hodName, uint256 _numberOfStudents, uint256 _numberOfTeachers, string[] memory _subjectsOffered, Student[] memory _students, Teacher[] memory _teachers) public {
        require(!department.isActive, "A department is already registered.");
        department = Department({
            name: _name,
            hodName: _hodName,
            numberOfStudents: _numberOfStudents,
            numberOfTeachers: _numberOfTeachers,
            subjectsOffered: _subjectsOffered,
            students: _students,
            teachers: _teachers,
            isActive: true
        });
    }

    function getDepartmentDetails() public view returns (string memory, string memory, uint256, uint256, Student[] memory, Teacher[] memory) {
        require(department.isActive, "No department is currently registered.");
        return (department.name, department.hodName, department.numberOfStudents, department.numberOfTeachers, department.students, department.teachers);
    }
    function updateDepartmentDetails(string memory _name, string memory _hodName, uint256 _numberOfStudents, uint256 _numberOfTeachers, Student[] memory _students, Teacher[] memory _teachers) public {
        require(department.isActive, "No department is currently registered.");
        department.name = _name;
        department.hodName = _hodName;
        department.numberOfStudents = _numberOfStudents;
        department.numberOfTeachers = _numberOfTeachers;
        department.students = _students;
        department.teachers = _teachers;
    }

    function deactivateDepartment() public {
        require(msg.sender == owner, "Only the contract owner can deactivate a department.");
        require(department.isActive, "No department is currently registered.");
        department.isActive = false;
    }

    function isDepartmentActive() public view returns (bool) {
        return department.isActive;
    }

    function getStudentCount() public view returns (uint256) {
        return students.length;
    }
    function getTeacherCount() public view returns (uint256) {
        return teachers.length;
    }
    function getDepartmentCount() public pure returns (uint256) {
        return 1; // Since only one department can be registered in this contract
    }

    function addStudentToList(string memory _name, string memory _emailId, uint256 _age, string memory _usn, string memory _department, string[] memory _subjects, string memory _teacherName) public {
        Student memory newStudent = Student({
            name: _name,
            emailId: _emailId,
            age: _age,
            usn: _usn,
            department: _department,
            subjects: _subjects,
            isEnrolled: true,
            teacherName: _teacherName,
            suspensionReason: "",
            suspensionTimestamp: 0,
            suspensionDuration: 0
        });
        students.push(newStudent);
    }
    function addTeacherToList(string memory _name, string memory _emailId, uint256 _age, string memory _department, string[] memory _subjects) public {
        Teacher memory newTeacher = Teacher({
            name: _name,
            emailId: _emailId,
            age: _age,
            department: _department,
            subjects: _subjects,
            isHired: true
        });
        teachers.push(newTeacher);
    }

    function clearStudentList() public {
        require(msg.sender == owner, "Only the contract owner can clear the student list.");
        delete students;
    }

    function clearTeacherList() public {
        require(msg.sender == owner, "Only the contract owner can clear the teacher list.");
        delete teachers;
    }


    function suspendTeacher(string memory _name) public {
        require(msg.sender == owner, "Only the contract owner can suspend a teacher.");
        require(bytes(_name).length > 0, "Teacher name must be provided.");
        require(teacher.isHired, "No teacher is currently registered.");
        require(keccak256(abi.encodePacked(teacher.name)) == keccak256(abi.encodePacked(_name)), "Teacher name does not match the registered teacher.");
        teacher.isHired = false;
    }

    function isTeacherSuspended() public view returns (bool) {
        return !teacher.isHired;
    }

    function reinstateTeacher(string memory _name) public {
        require(msg.sender == owner, "Only the contract owner can reinstate a teacher.");
        require(bytes(_name).length > 0, "Teacher name must be provided.");
        require(!teacher.isHired, "The teacher is not suspended.");
        require(keccak256(abi.encodePacked(teacher.name)) == keccak256(abi.encodePacked(_name)), "Teacher name does not match the registered teacher.");
        teacher.isHired = true;
    }

    function getSuspensionDetails() public view returns (string memory, uint256, uint256) {
        require(!student.isEnrolled, "The student is not suspended.");
        return (student.suspensionReason, student.suspensionTimestamp, student.suspensionDuration);
    }


    function getTeacherSubjects() public view returns (string[] memory) {
        require(teacher.isHired, "No teacher is currently registered.");
        return teacher.subjects;
    }
    function getStudentSubjects() public view returns (string[] memory) {
        require(student.isEnrolled, "No student is currently registered.");
        return student.subjects;
    }

    function getDepartmentSubjects() public view returns (string[] memory) {
        require(department.isActive, "No department is currently registered.");
        return department.subjectsOffered;
    }

    function sackTeacher(string memory _name) public {
        require(msg.sender == owner, "Only the contract owner can sack a teacher.");
        require(teacher.isHired, "No teacher is currently registered.");
        require(keccak256(abi.encodePacked(teacher.name)) == keccak256(abi.encodePacked(_name)), "Teacher name does not match the registered teacher.");
        delete teacher;
    }
}
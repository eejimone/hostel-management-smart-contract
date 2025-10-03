// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;



contract HostelManagement {
    string public schoolName;
    string public hostelName;
    string public location;
    string public hostelManager;
    uint256 public totalRooms;
    uint256 public occupiedRooms;
    uint256 public availableRooms;
    uint256 public roomPricePerMonth;
    string public roomOccupier;
    string public studentName;
    uint256 public studentAge;
    string public studentGender;
    string public studentContact;
    string public studentAddress;
    string public roomNo;
    


    address payable hostelWalletAddress;
    uint256 private hostelWalletBalance;
    mapping(address => uint256) private studentBalances;
    mapping(address => bool) private isStudentRegistered;
    mapping(address => bool) private hasRoomBooked;
    mapping(address => bool) private isStudentSuspended;
    mapping(address => bool) private hasPaid;
    mapping(address => uint256) private studentRoomNo;



    string public wardenName;
    string public wardenContact;
    string public wardenEmail;





    struct Database {
        string studentName;
        uint256 studentAge;
        string studentGender;
        string studentContact;
        string studentAddress;
        uint256 roomPricePerMonth;
        bool isRoomBooked;
        string roomStatus;
        string roomOccupier;
        string extraInfo;
    }

    Database[] public databases;

    bool public isRoomBooked;

    constructor(
        string memory _schoolName,
        string memory _hostelName,
        string memory _location,
        string memory _hostelManager,
        uint256 _totalRooms,
        uint256 _roomPricePerMonth
    ) {
        schoolName = _schoolName;
        hostelName = _hostelName;
        location = _location;
        hostelManager = _hostelManager;
        totalRooms = _totalRooms;
        roomPricePerMonth = _roomPricePerMonth;
        availableRooms = _totalRooms;
        roomBooked = false;
        occupiedRooms = 0;
        isRoomBooked = false;

    }
    bool public roomBooked;

    event RoomBooked(
        string studentName,
        uint256 studentAge,
        string studentGender,
        string studentContact,
        string studentAddress,
        uint256 roomPricePerMonth
    );
    event RoomVacated(string studentName, uint256 refundAmount);
    event HostelDetailsUpdated(
        string schoolName,
        string hostelName,
        string location,
        string hostelManager,
        uint256 totalRooms,
        uint256 roomPricePerMonth
    );
    event RoomPaid(string studentName, uint256 amountPaid);
    event StudentDetailsUpdated(
        string studentName,
        uint256 studentAge,
        string studentGender,
        string studentContact,
        string studentAddress
    );
    event StudentSuspended(string studentName, string reason);


    struct Student {
        string name;
        uint256 age;
        string gender;
        string contact;
        string homeAddress;
    }

    Student public student;

    enum RoomStatus {Available, Occupied, Maintenance, Reserved}
    RoomStatus public roomStatus;


    function registerStudent(string memory _studentName, uint256 _studentAge, string memory _studentGender, string memory _studentContact, string memory _studentAddress) public {
        student.name = _studentName;
        student.age = _studentAge;
        student.gender = _studentGender;
        student.contact = _studentContact;
        student.homeAddress = _studentAddress;


        require(availableRooms > 0, "No rooms available");
        require(!roomBooked, "Room already booked");
        roomBooked = true;
        occupiedRooms += 1;
        availableRooms -= 1;
        roomStatus = RoomStatus.Occupied;
        emit RoomBooked(student.name, student.age, student.gender, student.contact, student.homeAddress, roomPricePerMonth);
    }


    function vacateRoom() public {
        require(roomStatus == RoomStatus.Occupied, "Room is not occupied");
        isRoomBooked = false;
        occupiedRooms -= 1;
        availableRooms += 1;
        roomStatus = RoomStatus.Available;
        emit RoomVacated(student.name, roomPricePerMonth);
    }




    function checkAvailability() public view returns (uint256) {
        return availableRooms;
    }

    function makePayment() public payable {
        require(roomStatus == RoomStatus.Occupied, "Room is not occupied");
        require(msg.value >= roomPricePerMonth, "Insufficient payment");
        hostelWalletAddress.transfer(msg.value);
        studentBalances[msg.sender] += msg.value;
        hasPaid[msg.sender] = true;
        emit RoomPaid(student.name, msg.value);
    }


    function updateHostelDetails(
        string memory _schoolName,
        string memory _hostelName,
        string memory _location,
        string memory _hostelManager,
        uint256 _totalRooms,
        uint256 _roomPricePerMonth
    ) public {
        schoolName = _schoolName;
        hostelName = _hostelName;
        location = _location;
        hostelManager = _hostelManager;
        totalRooms = _totalRooms;
        roomPricePerMonth = _roomPricePerMonth;
        availableRooms = totalRooms - occupiedRooms;
        emit HostelDetailsUpdated(schoolName, hostelName, location, hostelManager, totalRooms, roomPricePerMonth);
    }



    function updateStudentDetails(
        string memory _studentName,
        uint256 _studentAge,
        string memory _studentGender,
        string memory _studentContact,
        string memory _studentAddress
    ) public {
        student.name = _studentName;
        student.age = _studentAge;
        student.gender = _studentGender;
        student.contact = _studentContact;
        student.homeAddress = _studentAddress;
        emit StudentDetailsUpdated(student.name, student.age, student.gender, student.contact, student.homeAddress);
    }


    function getStudentDetails() public view returns(string memory, uint256, string memory, string memory, string memory) {
        return (student.name, student.age, student.gender, student.contact, student.homeAddress);
    }


    function suspendStudent(string memory _studentName, string memory /* reason */) public {
        require(keccak256(abi.encodePacked(student.name)) == keccak256(abi.encodePacked(_studentName)), "Student not found");
        vacateRoom();
        student.name = "";
        student.age = 0;
        student.gender = "";
        student.contact = "";
        student.homeAddress = "";
        emit StudentSuspended(_studentName, /* reason */ "");
    }
    event databaseUpdated(string studentName, uint256 studentAge, string studentGender, string studentContact, string studentAddress, uint256 roomPricePerMonth);
    function storeInDataBase() public {
        emit databaseUpdated(student.name, student.age, student.gender, student.contact, student.homeAddress, roomPricePerMonth);
    }

    function bookRooms(uint256 numberOfRooms) public {
        require(numberOfRooms > 0, "Number of rooms must be greater than zero");
        require(availableRooms >= numberOfRooms, "Not enough rooms available");
        require(!isRoomBooked, "Room already booked");
        isRoomBooked = true;
        occupiedRooms += numberOfRooms;
        availableRooms -= numberOfRooms;
        roomStatus = RoomStatus.Occupied;
        emit RoomBooked(student.name, student.age, student.gender, student.contact, student.homeAddress, roomPricePerMonth);
    }
    function getRoomStatus() public view returns (string memory) {
        string[4] memory statusStrings = ["Available", "Occupied", "Maintenance", "Reserved"];
        return statusStrings[uint256(roomStatus)];
    }
}



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

    bool public isRoomBooked;

}
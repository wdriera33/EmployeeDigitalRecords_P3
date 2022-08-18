pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract EmployeeRegistry is ERC721Full {
    constructor() public ERC721Full("EmployeeRegistryToken", "ERT") {}

    struct Employee {
        address owner;
        string name;
        string birthYear;
        string originalCdlYear;
        string violations;
        string accidents;
        uint256 employeeScore;
        string attachment;
    }

    mapping(uint256 => Employee) public employeeData;

    event Score(uint256 tokenId, uint256 employeeScore, string violations, string accidents, string reportURI, string attachment);
    
    function imageUri(
        uint256 tokenId

    ) public view returns (string memory imageJson){
        return employeeData[tokenId].attachment;
    }


    function onboardingEmployee(
        address owner,
        string memory name,
        string memory birthYear,
        string memory originalCdlYear,
        string memory violations,
        string memory accidents,
        uint256 initialEmployeeScore,
        string memory attachment
       
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, attachment);

        employeeData[tokenId] = Employee(owner, name, birthYear, originalCdlYear, violations, accidents, initialEmployeeScore, attachment);

        return tokenId;
    }

    function updateRecord(
        uint256 tokenId,
        uint256 newEmployeeScore,
        string memory newAccidents,
        string memory newViolations,
        string memory reportURI,
        string memory attachment
        
    ) public returns (uint256) {
        employeeData[tokenId].employeeScore = newEmployeeScore;
        employeeData[tokenId].accidents = newAccidents;
        employeeData[tokenId].violations = newViolations;
        
        emit Score(tokenId, newEmployeeScore, newViolations, newAccidents, reportURI, attachment);

        return (employeeData[tokenId].employeeScore);
    }
}

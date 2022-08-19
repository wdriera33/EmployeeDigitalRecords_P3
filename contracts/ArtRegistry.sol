pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract EmployeeRegistry is ERC721Full {
    constructor() public ERC721Full("EmployeeRegistryToken", "ERT") {}

    struct Ertwork {
        string name;
        string birthyear;
        string originalCdlYear;
        string employeeViolations;
        string employeeAccidents;
        uint256 scoreValue;
        string ertJson;
    }

    mapping(uint256 => Ertwork) public employeeRecords;

    event Score(uint256 tokenId, uint256 scoreValue, string reportURI, string ertJson);
    
    function imageUri(
        uint256 tokenId

    ) public view returns (string memory imageJson){
        return employeeRecords[tokenId].ertJson;
    }


    function registerEmployee(
        address owner,
        string memory name,
        string memory birthyear,
        string memory originalCdlYear,
        string memory employeeViolations,
        string memory employeeAccidents,
        uint256 initialScoreValue,
        string memory tokenURI,
        string memory tokenJSON
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        employeeRecords[tokenId] = Ertwork(name, birthyear, originalCdlYear, employeeViolations, employeeAccidents, initialScoreValue, tokenJSON);

        return tokenId;
    }

    function newScore(
        uint256 tokenId,
        uint256 newScoreValue,
        string memory reportURI,
        string memory tokenJSON
        
    ) public returns (uint256) {
        employeeRecords[tokenId].scoreValue = newScoreValue;

        emit Score(tokenId, newScoreValue, reportURI, tokenJSON);

        return (employeeRecords[tokenId].scoreValue);
    }
}
// SPDX-License-Identifier: MIT

pragma solidity 0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721URIStorage, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyHash;
    uint256 public fee;
    enum Language {
        Chinese,
        English
    }
    mapping(uint256 => Language) public tokenIdToLanguage;
    mapping(bytes32 => address) public requestIdToSender;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event languageAssigned(uint256 indexed tokenId, Language language);

    constructor(
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyHash
    ) public VRFConsumerBase(_vrfCoordinator, _link) ERC721("Mark", "MGB") {
        tokenCounter = 0;
        keyHash = _keyHash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 _randomness)
        internal
        override
    {
        require(_randomness > 0, "random-not-found");
        Language language = Language(_randomness % 2);
        uint256 newTokenId = tokenCounter;
        tokenIdToLanguage[newTokenId] = language;
        emit languageAssigned(newTokenId, language);
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 _tokenId, string memory _tokenURI) public {
        // Chinese, English
        require(
            _isApprovedOrOwner(_msgSender(), _tokenId),
            "ERC721: transfer caller is not owner or approved"
        );
        _setTokenURI(_tokenId, _tokenURI);
    }
}

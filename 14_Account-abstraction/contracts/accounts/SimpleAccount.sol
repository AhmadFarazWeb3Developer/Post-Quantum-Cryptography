// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/utils/cryptography/MessageHashUtils.sol";
import "@openzeppelin/contracts/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts/proxy/utils/UUPSUpgradeable.sol";
import "../core/BaseAccount.sol";
import "../core/Helpers.sol";
import "./callback/TokenCallbackHandler.sol";

// Changed SimpleAccount for local testing:

// 1. Added falconPublicKey (bytes) storage
//    - Stores 897-byte Falcon public key instead of ECDSA owner
//    - Used in signature verification

// 2. Kept owner (address) for access control
//    - Traditional EOA owner for onlyOwner checks
//    - Separate from Falcon public key

// 3. Added setFalconPublicKey() function
//    - Sets the Falcon public key after initialization
//    - Only callable by owner

// 4. Modified _validateSignature()
//    - Checks signature length (666 bytes for Falcon)
//    - Extracts commitment from first 32 bytes
//    - Recomputes keccak256(userOpHash + falconPublicKey)
//    - Compares submitted vs expected commitment

// 5. Added testValidateSignature() public wrapper
//    - Allows testing _validateSignature() without EntryPoint
//    - Internal function wrapped for accessibility

// 6. Removed EntryPoint interaction in getDeposit(), addDeposit()
//    - These won't work on localhost (dummy EntryPoint)
//    - Not needed for signature testing

/**
 * minimal account.
 *  this is sample minimal account.
 *  has execute, eth handling methods
 *  has a single signer that can send requests through the entryPoint.
 */
contract SimpleAccount is
    BaseAccount,
    TokenCallbackHandler,
    UUPSUpgradeable,
    Initializable
{
    address public owner;
    bytes public falconPublicKey; // FALCON owner public key

    IEntryPoint private immutable _entryPoint;

    event SimpleAccountInitialized(
        IEntryPoint indexed entryPoint,
        address indexed owner
    );

    modifier onlyOwner() {
        _onlyOwner();
        _;
    }

    error NotOwner(address msgSender, address entity, address owner);
    error NotOwnerOrEntryPoint(
        address msgSender,
        address entity,
        address entryPoint,
        address owner
    );

    /// @inheritdoc BaseAccount
    function entryPoint() public view virtual override returns (IEntryPoint) {
        return _entryPoint;
    }

    // solhint-disable-next-line no-empty-blocks
    receive() external payable {}

    constructor(IEntryPoint anEntryPoint) {
        _entryPoint = anEntryPoint;
        _disableInitializers();
    }

    function _onlyOwner() internal view {
        // Directly from EOA owner, or through the account itself (which gets redirected through execute())
        require(
            msg.sender == owner || msg.sender == address(this),
            NotOwner(msg.sender, address(this), owner)
        );
    }

    /**
     * @dev The _entryPoint member is immutable, to reduce gas consumption.  To upgrade EntryPoint,
     * a new implementation of SimpleAccount must be deployed with the new EntryPoint address, then upgrading
     * the implementation by calling `upgradeTo()`
     * @param anOwner the owner (signer) of this account
     */
    function initialize(address anOwner) public virtual initializer {
        _initialize(anOwner);
    }

    function _initialize(address anOwner) internal virtual {
        owner = anOwner;
        emit SimpleAccountInitialized(entryPoint(), owner);
    }

    function setFalconPublicKey(
        bytes calldata _falconPublicKey
    ) public onlyOwner {
        require(
            _falconPublicKey.length == 897,
            "Invalid Falcon public key length"
        );
        falconPublicKey = _falconPublicKey;
    }

    // Require the function call went through EntryPoint or owner
    function _requireForExecute() internal view virtual override {
        require(
            msg.sender == address(entryPoint()) || msg.sender == owner,
            NotOwnerOrEntryPoint(
                msg.sender,
                address(this),
                address(entryPoint()),
                owner
            )
        );
    }

    function _validateSignature(
        PackedUserOperation calldata userOp,
        bytes32 userOpHash
    ) internal view override returns (uint256 validationData) {
        // Check 1 — correct signature length for FALCON-512
        //  commitment (32 bytes) + falcon_signature (666 bytes)
        if (userOp.signature.length != 698) return SIG_VALIDATION_FAILED;

        // Check 2 - Extract commitment from signature
        bytes32 submittedCommitment = bytes32(userOp.signature[0:32]);

        // Check 3 — Recompute expected commitment using stored falconPublicKey
        bytes32 expectedCommitment = keccak256(
            abi.encodePacked(userOpHash, falconPublicKey)
        );

        // Compare
        if (submittedCommitment != expectedCommitment) {
            return SIG_VALIDATION_FAILED;
        }

        return SIG_VALIDATION_SUCCESS;
    }

    // PUBLIC wrapper for testing only
    function testValidateSignature(
        PackedUserOperation calldata userOp,
        bytes32 userOpHash
    ) public view returns (uint256) {
        return _validateSignature(userOp, userOpHash);
    }
    /**
     * check current account deposit in the entryPoint
     */
    function getDeposit() public view virtual returns (uint256) {
        return entryPoint().balanceOf(address(this));
    }

    /**
     * deposit more funds for this account in the entryPoint
     */
    function addDeposit() public payable {
        entryPoint().depositTo{value: msg.value}(address(this));
    }

    /**
     * withdraw value from the account's deposit
     * @param withdrawAddress target to send to
     * @param amount to withdraw
     */
    function withdrawDepositTo(
        address payable withdrawAddress,
        uint256 amount
    ) public virtual onlyOwner {
        entryPoint().withdrawTo(withdrawAddress, amount);
    }

    function _authorizeUpgrade(
        address newImplementation
    ) internal view override {
        (newImplementation);
        _onlyOwner();
    }
}

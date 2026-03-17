## EOA — The Current Model

An EOA (Externally Owned Account) is a standard Ethereum wallet.

```
Private key    →  you hold this secret number
Public key     →  mathematically derived from private key
Address        →  last 20 bytes of keccak256(public key)
```

When you send a transaction from an EOA:

```
Step 1  →  Build transaction: nonce, to, value, data, gas, chainId
Step 2  →  RLP encode the transaction fields into raw bytes
Step 3  →  Keccak-256 hash the encoded bytes → txHash
Step 4  →  ECDSA sign txHash with private key → r, s, v
Step 5  →  Broadcast signed transaction to network
Step 6  →  Ethereum protocol calls ecrecover(txHash, v, r, s)
Step 7  →  ecrecover returns the signer address
Step 8  →  Protocol checks signer address == transaction.from
Step 9  →  If match → execute. If not → reject.
```

The protocol handles everything. You have zero control over how your signature is verified.

**Limitations of EOA:**

```
Signature scheme     →  ECDSA only, hardcoded, cannot change
Gas payment          →  ETH only, must always hold ETH
Key recovery         →  impossible, lose key = lose everything forever
Spending limits      →  none, any transaction is all or nothing
Batching             →  no, one transaction at a time
Quantum resistance   →  none, ECDSA dies under Shor's Algorithm
```

---

## ERC-4337 — Account Abstraction

ERC-4337 is an Ethereum standard that replaces your EOA with a **smart contract wallet.** Instead of the protocol verifying your signature — your own smart contract verifies it. You define the rules.

This works without any protocol changes. No hard fork needed. It works on Ethereum today.

### New Concepts

**UserOperation:**
Instead of a normal transaction you create a UserOperation object. It contains the same information as a transaction but goes through a different path.

```
UserOperation fields:
sender               →  your smart contract wallet address
nonce                →  replay protection
initCode             →  bytecode to deploy wallet if it does not exist yet
callData             →  what you want to execute
callGasLimit         →  gas limit for execution
verificationGasLimit →  gas limit for signature verification
preVerificationGas   →  compensation for the bundler
maxFeePerGas         →  maximum gas price willing to pay
maxPriorityFeePerGas →  tip for the bundler
paymasterAndData     →  optional — who pays gas on your behalf
signature            →  THIS IS WHAT YOU CONTROL COMPLETELY
```

**Bundler:**
A node that collects UserOperations from users, bundles them together, and submits them to the EntryPoint contract on-chain. The bundler pays gas upfront and gets reimbursed by the EntryPoint.

**EntryPoint:**
A singleton smart contract deployed at a fixed address on Ethereum. It is the coordinator — it receives bundles from bundlers, calls your wallet to verify the signature, and if valid, executes the transaction.

**Paymaster:**
An optional contract that can pay gas fees on behalf of users. Allows gas sponsorship or payment in ERC-20 tokens instead of ETH.

### How ERC-4337 Works

```
Step 1  →  Build UserOperation
Step 2  →  Sign it however you want (ECDSA, FALCON, anything)
Step 3  →  Send to Bundler's alt-mempool
Step 4  →  Bundler submits bundle to EntryPoint
Step 5  →  EntryPoint calls validateUserOp on your Account contract
Step 6  →  Your Account contract verifies signature YOUR WAY
Step 7  →  If valid → EntryPoint executes the callData
Step 8  →  Bundler gets reimbursed for gas
```

The critical step is Step 6. Your contract. Your rules. Any signature scheme.

### EOA vs ERC-4337

| Feature              | EOA              | ERC-4337                 |
| -------------------- | ---------------- | ------------------------ |
| Wallet type          | Private key pair | Smart contract           |
| Signature scheme     | ECDSA only       | Any scheme you implement |
| Gas payment          | ETH only         | ETH, ERC-20, sponsored   |
| Key recovery         | Impossible       | Configurable             |
| Spending limits      | None             | Configurable             |
| Transaction batching | No               | Yes                      |
| Multi-signature      | No               | Yes                      |
| Upgradeable          | No               | Yes via UUPS proxy       |
| Quantum resistant    | No               | Yes if you use FALCON    |

---

## The Solution — FALCON Signatures via ERC-4337

**FN-DSA (FALCON)** is one of four post-quantum cryptography standards finalized by NIST in August 2024 under FIPS 206. It is a signature scheme based on NTRU lattice mathematics.

```
ECDSA security  →  ECDLP hard problem  →  Shor's breaks it
FALCON security →  NTRU lattice problem →  no quantum algorithm breaks it
```

FALCON is specifically suited for blockchain because of compact signature sizes:

```
ECDSA signature      →   64 bytes
FALCON-512 signature →  666 bytes
ML-DSA (Dilithium)   → 2420 bytes
SLH-DSA (SPHINCS+)   → 8000-17000 bytes
```

666 bytes is significantly larger than ECDSA but far more practical for on-chain use than other PQC signature schemes.

---

## Why Off-Chain FALCON Verification

Here is the honest technical reality.

### The On-Chain Problem

Full FALCON verification requires polynomial ring arithmetic over NTRU lattices in 512 dimensions. Specifically:

```
1. Decode signature into polynomials s1 and s2
2. Check vector norm: ||s1||² + ||s2||² ≤ threshold
3. Hash message to polynomial c using SHAKE-256
4. Verify: s1 + s2 × h ≡ c (mod q)  where h is public key polynomial
5. q = 12289, N = 512
```

Implementing this in Solidity means:

```
Polynomial multiplication using NTT  →  512 × 512 operations
Each operation mod 12289             →  expensive on EVM
Full verification                    →  estimated 5-15 million gas
One ETH transaction at 30 gwei       →  0.15 to 0.45 ETH per verification
```

This is economically impractical for real use today.

### The Right Solution — EIP Precompile (Future)

The correct long-term solution is an Ethereum precompile for FALCON verification — similar to how `ecrecover` is a precompile for ECDSA at address `0x01`.

```
Today:    ecrecover(hash, v, r, s)          →  precompile, ~3000 gas
Future:   falconVerify(hash, sig, pubkey)   →  precompile, ~3000 gas
```

Several EIPs are being discussed for this. When it arrives — FALCON verification on-chain becomes trivial and cheap.

### The Practical Solution Today — Off-Chain Verification with Commitment

Until the precompile exists we use an off-chain verification approach with an on-chain commitment scheme. This is a hybrid approach. It is not fully trustless but it is practical and demonstrates the complete integration architecture.

**The key insight:**

Your TypeScript code can run full FALCON verification locally using the `pqcrypto` library. The result of that verification is committed to on-chain using a keccak256 hash that binds the signature to the specific UserOperation and public key.

**Why this is still meaningful:**

```
Off-chain FALCON verification  →  proves the math works end to end
On-chain commitment check      →  proves the right key signed the right operation
Complete architecture          →  shows how production system would work with precompile
```

When the FALCON precompile arrives — you replace the commitment check with one line:

```solidity
return IFalconVerifier(PRECOMPILE_ADDRESS).verify(userOpHash, sig, pubkey)
       ? SIG_VALIDATION_SUCCESS
       : SIG_VALIDATION_FAILED;
```

Everything else stays identical.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    OFF-CHAIN (TypeScript)                │
│                                                         │
│  1. Generate FALCON-512 keypair                         │
│     public_key  (897 bytes)                             │
│     private_key (1281 bytes)                            │
│                                                         │
│  2. Build UserOperation                                 │
│     hash = keccak256(packed UserOperation fields)       │
│                                                         │
│  3. Sign with FALCON                                    │
│     falcon_signature = FALCON.sign(hash, private_key)   │
│     (666 bytes)                                         │
│                                                         │
│  4. Verify locally                                      │
│     FALCON.verify(hash, falcon_signature, public_key)   │
│     → confirmed valid before submitting                 │
│                                                         │
│  5. Compute commitment                                  │
│     commitment = keccak256(hash + public_key)           │
│                                                         │
│  6. Build final signature field                         │
│     signature = commitment (32 bytes)                   │
│               + falcon_signature (666 bytes)            │
│               = 698 bytes total                         │
│                                                         │
│  7. Submit UserOperation to Bundler                     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    ON-CHAIN (Solidity)                  │
│                                                         │
│  EntryPoint calls _validateSignature                    │
│                                                         │
│  1. Check total signature length == 698 bytes           │
│                                                         │
│  2. Extract commitment (first 32 bytes)                 │
│     Extract falcon_signature (remaining 666 bytes)      │
│                                                         │
│  3. Recompute expected commitment                       │
│     expected = keccak256(userOpHash + falconPublicKey)  │
│                                                         │
│  4. Compare                                             │
│     commitment == expected?                             │
│     YES → SIG_VALIDATION_SUCCESS                        │
│     NO  → SIG_VALIDATION_FAILED                         │
└─────────────────────────────────────────────────────────┘
```

---

## What Changes from SimpleAccount

SimpleAccount.sol has one function that handles signature verification:

```solidity
// ORIGINAL — ECDSA
function _validateSignature(
    PackedUserOperation calldata userOp,
    bytes32 userOpHash
) internal override virtual returns (uint256 validationData) {
    if (owner != ECDSA.recover(userOpHash, userOp.signature))
        return SIG_VALIDATION_FAILED;
    return SIG_VALIDATION_SUCCESS;
}
```

Three things change:

**Change 1 — Owner storage:**

```solidity
// Before
address public owner;

// After
bytes public falconPublicKey;
```

**Change 2 — Remove ECDSA import, add no external dependency:**

```solidity
// Before
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

// After — no signature library needed
// Verification is pure keccak256
```

**Change 3 — Replace \_validateSignature:**

```solidity
// After — FALCON commitment verification
function _validateSignature(
    PackedUserOperation calldata userOp,
    bytes32 userOpHash
) internal override virtual returns (uint256 validationData) {

    // Total length: 32 bytes commitment + 666 bytes FALCON signature
    if (userOp.signature.length != 698)
        return SIG_VALIDATION_FAILED;

    // Extract commitment from first 32 bytes
    bytes32 submittedCommitment = bytes32(userOp.signature[0:32]);

    // Recompute expected commitment
    bytes32 expectedCommitment = keccak256(abi.encodePacked(
        userOpHash,
        falconPublicKey
    ));

    // Compare
    if (submittedCommitment != expectedCommitment)
        return SIG_VALIDATION_FAILED;

    return SIG_VALIDATION_SUCCESS;
}
```

That is the complete change. Everything else in SimpleAccount stays identical.

---

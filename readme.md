# Complete Cryptography Reference

> By Ahmad Faraz | PQC Journey

---

## The 3 Jobs of Cryptography

Everything in cryptography does one of three jobs:

| Job                            | Simple Meaning                                           | Example        |
| ------------------------------ | -------------------------------------------------------- | -------------- |
| **Confidentiality**            | Hide the message so only receiver can read it            | Encryption     |
| **Integrity + Authentication** | Prove who sent it and it was not tampered                | Signatures     |
| **Key Exchange**               | Two parties agree on a shared secret over public channel | Diffie-Hellman |

---

## Job 1 — Encryption (Confidentiality)

> "Only the intended receiver can read this"

### Secret Key / Symmetric Encryption

Both sender and receiver use the **same key**.

```
Sender:   Encrypt(message, key)   → ciphertext
Receiver: Decrypt(ciphertext, key) → message
```

**Algorithms:**

- AES-128
- AES-256 ← quantum safe, use this
- ChaCha20

**Problem:** How do you share that key securely in the first place? → This is why Key Exchange exists.

---

### Public Key / Asymmetric Encryption

Sender uses receiver's **public key** to encrypt.
Only receiver's **private key** can decrypt.

```
Sender:   Encrypt(message, receiver_public_key)  → ciphertext
Receiver: Decrypt(ciphertext, receiver_private_key) → message
```

**Algorithms:**

- RSA Encryption ← broken by Shor's
- ElGamal ← broken by Shor's

**Important:** RSA here is used to HIDE data. Not to sign it. Different job, same algorithm name — this is where confusion happens.

---

## Job 2 — Digital Signatures (Authentication + Integrity)

> "Prove you wrote this and nobody changed it"

Sender uses their own **private key** to sign.
Anyone uses sender's **public key** to verify.

```
Sender:   Sign(message, my_private_key)       → signature
Receiver: Verify(message, signature, my_public_key) → valid or invalid
```

**Algorithms:**

- RSA Signatures ← broken by Shor's
- DSA ← broken by Shor's
- ECDSA ← broken by Shor's (what Ethereum uses)

**Important:** RSA here is used to PROVE IDENTITY. Not to hide data. Same algorithm name, completely different job. This is the confusion.

---

## RSA — Two Jobs, One Name (The Confusion Resolved)

RSA is a mathematical framework. It can do two completely different things:

|                          | RSA Encryption            | RSA Signature         |
| ------------------------ | ------------------------- | --------------------- |
| **Job**                  | Hide data                 | Prove identity        |
| **Who uses public key**  | Sender (to encrypt)       | Verifier (to verify)  |
| **Who uses private key** | Receiver (to decrypt)     | Signer (to sign)      |
| **Question it answers**  | "Can only you read this?" | "Did you write this?" |
| **Broken by Shor's**     | Yes                       | Yes                   |
| **Replaced by**          | Kyber                     | Dilithium / FALCON    |

Same math underneath. Completely different purpose. This is why the name confused you.

---

## Job 3 — Key Exchange

> "Agree on a shared secret without ever sending it"

Two parties generate a shared secret over a public channel. An eavesdropper watching everything cannot figure out the secret.

```
Alice and Bob both end up with: shared_secret
Eve watching the conversation:  sees nothing useful
```

After key exchange both parties use shared_secret with AES-256 for actual encryption.

**Algorithms:**

- Diffie-Hellman ← broken by Shor's
- ECDH (Elliptic Curve Diffie-Hellman) ← broken by Shor's
- Kyber (ML-KEM) ← quantum safe ✓

---

## Hashing — Not Encryption, Not Signatures

> "Create a unique fingerprint of data"

One way only. Cannot reverse it. Same input always gives same output.

```
SHA-256("hello") → 2cf24dba5fb0a30e...  (always the same)
SHA-256("hellp") → completely different  (one letter change = totally different hash)
```

**Used for:**

- Verifying file integrity
- Storing passwords
- Blockchain block linking
- Inside signature algorithms

**Algorithms:**

- SHA-256 ← quantum safe ✓
- SHA-3 ← quantum safe ✓
- SHA-512 ← very safe ✓
- MD5 ← broken (not by quantum, just old)

**Hashing is NOT encryption.** You cannot decrypt a hash. It is a one-way fingerprint.

---

## Complete Map — Classical vs Post-Quantum

### What Quantum Breaks:

| Job          | Classical Algorithm | Broken By | Replacement               |
| ------------ | ------------------- | --------- | ------------------------- |
| Key Exchange | Diffie-Hellman      | Shor's    | Kyber                     |
| Key Exchange | ECDH                | Shor's    | Kyber                     |
| Signatures   | RSA Signatures      | Shor's    | Dilithium / FALCON        |
| Signatures   | ECDSA               | Shor's    | Dilithium / FALCON        |
| Signatures   | DSA                 | Shor's    | Dilithium / FALCON        |
| Encryption   | RSA Encryption      | Shor's    | Kyber (key encapsulation) |

### What Quantum Does NOT Break:

| Job                  | Algorithm | Why Safe                                       |
| -------------------- | --------- | ---------------------------------------------- |
| Symmetric Encryption | AES-256   | Grover's only halves security, 128-bit remains |
| Hashing              | SHA-256   | Grover's only halves security, 128-bit remains |
| Hashing              | SHA-3     | Same reason                                    |
| Hashing              | SHA-512   | Even safer — 256-bit remains after Grover's    |

---

## The 4 NIST PQC Standards

| Algorithm          | Job          | Replaces              | Based On       | Standard |
| ------------------ | ------------ | --------------------- | -------------- | -------- |
| Kyber (ML-KEM)     | Key Exchange | Diffie-Hellman, ECDH  | Lattice (RLWE) | FIPS 203 |
| Dilithium (ML-DSA) | Signatures   | ECDSA, RSA Signatures | Lattice (RLWE) | FIPS 204 |
| SPHINCS+ (SLH-DSA) | Signatures   | ECDSA, RSA Signatures | Hash Functions | FIPS 205 |
| FALCON             | Signatures   | ECDSA (compact)       | Lattice (NTRU) | FIPS 206 |

---

## For Blockchain Specifically

| Blockchain Need                | Classical       | PQC Replacement          |
| ------------------------------ | --------------- | ------------------------ |
| Transaction signing (Ethereum) | ECDSA secp256k1 | Dilithium or FALCON      |
| Wallet key generation          | secp256k1       | Dilithium or FALCON      |
| Key agreement protocols        | ECDH            | Kyber                    |
| Block hashing                  | SHA-256         | Already safe — no change |
| Compact signatures             | ECDSA           | FALCON                   |
| Most conservative choice       | DSA             | SPHINCS+                 |

---

## Two Quantum Weapons Summary

|              | Shor's Algorithm                      | Grover's Algorithm         |
| ------------ | ------------------------------------- | -------------------------- |
| Type         | Targeted attack                       | General speedup            |
| Breaks       | RSA, ECDSA, Diffie-Hellman completely | Weakens everything by half |
| Survives     | Nothing classical in public key       | AES-256, SHA-256, all PQC  |
| Fix          | Replace algorithm entirely            | Double key size            |
| Threat level | Existential for blockchain            | Manageable                 |

---

## One Paragraph — Everything

> Classical cryptography has three jobs: hide data (encryption), prove identity (signatures), and agree on secrets (key exchange). Quantum computers using Shor's Algorithm destroy every public key algorithm used for these jobs — RSA, ECDSA, Diffie-Hellman. Symmetric encryption like AES-256 and hashing like SHA-256 are already quantum safe and need no replacement. NIST standardized four post-quantum algorithms to replace the broken ones — Kyber for key exchange, Dilithium and FALCON for signatures, SPHINCS+ as a conservative backup. All of them run on normal computers but are mathematically designed so quantum computers cannot break them.

---

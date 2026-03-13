```
ECDSA broken by  → Shor's Algorithm (finds private key from public key)
Dilithium safe   → lattice LWE problem (Shor's cannot solve this)
```

**Key generation difference:**

Both Dilithium and SPHINCS+ generate public and private keys. Same interface. Completely different math underneath.

---

**Dilithium key generation:**

```
Private key = secret vector hidden in lattice
Public key  = that vector mixed with random lattice noise
Security    = finding private key requires solving LWE problem
```

---

**SPHINCS+ key generation:**

```
Private key = two random seeds (SK.seed and SK.prf)
Public key  = root of a massive Merkle tree of hashes
Security    = finding private key requires reversing SHA-256
```

---

**Simple picture:**

```
Dilithium:
private key → lattice vector → mixed with noise → public key

SPHINCS+:
private key → hash it → hash again → hash again × thousands → build tree → root = public key
```

---

**Same job. Different foundation:**

|              | Dilithium           | SPHINCS+         |
| ------------ | ------------------- | ---------------- |
| Private key  | Lattice vector      | Random seed      |
| Public key   | Noisy lattice point | Merkle tree root |
| Security     | LWE hard problem    | SHA-256 one-way  |
| If broken by | Lattice algorithm   | SHA-256 broken   |

---

**One line:**

> Both generate public and private keys for signing. Dilithium hides the private key in lattice math. SPHINCS+ hides it inside a tree of hashes. Same job, completely different hiding mechanism.

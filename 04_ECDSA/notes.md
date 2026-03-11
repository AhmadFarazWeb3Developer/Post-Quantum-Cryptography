# ECDSA & secp256k1 — Complete Notes

> By Ahmad Faraz | PQC Journey | Week 4

---

## 1. What is ECDSA

**Elliptic Curve Digital Signature Algorithm.**

It is how Ethereum proves:

> "This transaction was signed by the owner of this private key."

Three things it does:

1. Generate private and public key
2. Sign a message
3. Verify the signature

---

## 2. What is secp256k1

The specific elliptic curve that Bitcoin and Ethereum use under ECDSA.

### Name Breakdown

| Part  | Meaning                                       |
| ----- | --------------------------------------------- |
| `sec` | Standards for Efficient Cryptography          |
| `p`   | Prime field — math happens over prime numbers |
| `256` | 256 bits — the key size                       |
| `k`   | Koblitz curve — special efficient type        |
| `1`   | First curve of this kind by SECG              |

### The Curve Equation

```
y² = x³ + 7 (mod p)
```

Every valid key pair is a point `(x, y)` that satisfies this equation.
`mod p` keeps all calculations inside the finite field.

---

## 3. Key Terms

**SECG**
Standards for Efficient Cryptography Group. The organization that defined and standardized secp256k1. Like NIST but focused on elliptic curves.

**Finite Field**
Normal math goes to infinity. Finite field math stays within a fixed boundary — that boundary is a large prime number `p`. Every calculation does `mod p` to stay inside. This makes the math predictable and cryptographically secure.

**Koblitz Curve**
A special type of elliptic curve that allows faster computation. Reason Bitcoin and Ethereum chose it — efficiency matters when millions of transactions are verified every day.

**ECDLP — Elliptic Curve Discrete Logarithm Problem**
Given:

```
public_key = private_key × G
```

Find `private_key` from `public_key`.
Impossible classically. Shor's Algorithm solves it on quantum hardware.
This is the entire security assumption of Bitcoin and Ethereum.

---

## 4. The Generator Point G

### What is G

G is a fixed starting point on the secp256k1 curve. It is hardcoded into the standard. Every person using secp256k1 uses the exact same G. It is public — everyone knows it.

### How G was chosen

G was not randomly invented. It was carefully selected by SECG following strict criteria:

1. **It must lie on the curve** — the coordinates of G must satisfy `y² = x³ + 7 (mod p)`
2. **It must have a large prime order** — meaning if you keep adding G to itself, it takes an astronomically large number of steps before you cycle back to the starting point. That number of steps is called the order `n` and for secp256k1 it is a 256-bit prime number.
3. **It must be verifiably random** — SECG chose G so that no one could have a backdoor. The coordinates were derived from nothing-up-my-sleeve numbers to prove no hidden weakness.

### The actual G coordinates

```
G = (
  x: 79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
  y: 483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
)
```

These are hexadecimal numbers. Fixed forever. Hardcoded into every Bitcoin and Ethereum implementation.

---

## 5. How Keys Are Generated

### Private Key

Just a randomly generated 256-bit number. Nothing more.

```
private_key = random 256-bit number
example:     12345678  (real one is much larger)
```

### Public Key

Take the private key and multiply it by G on the curve.

```
public_key = private_key × G
```

The result is another point on the curve. That point is your public key.

### What does multiplying by G mean on a curve

It is not normal multiplication. It is called **Point Multiplication** or **Scalar Multiplication**. It works like this:

```
private_key = 4
public_key  = G + G + G + G   (add G to itself 4 times)
```

Each addition follows the elliptic curve addition rules — reflect, intersect, special geometry on the curve.

For a 256-bit private key this means adding G to itself an astronomically large number of times. Computers do this efficiently using a technique called **double and add**.

---

## 6. The Security

```
private_key × G = public_key    ← easy, milliseconds
public_key  / G = private_key   ← impossible classically
```

Going forward is easy. Going backward is the ECDLP. You cannot simply divide a point on a curve — there is no division operation. The only way to reverse it is to try every possible private key one by one. With 2^256 possibilities that takes longer than the age of the universe.

Until Shor's Algorithm.

---

## 7. How Signing Works

When you send an Ethereum transaction:

```
1. Hash your message         → get a number h
2. Pick a random number k
3. Calculate point R = k × G
4. Calculate s = (h + private_key × R) / k
5. Signature = (R, s)
```

The signature proves you own the private key without ever revealing it.

---

## 8. How Verification Works

The receiver has: message, signature `(R, s)`, your public key.

```
1. Recalculate using public_key and signature math
2. If result matches R → signature is valid
3. Message is authentic and untampered
```

No private key needed to verify. Public key is enough.

---

## 9. Address Generation

```
Random 256-bit number
        ↓
   private key
        ↓
private_key × G
        ↓
   public key (point on curve)
        ↓
   hash with Keccak-256
        ↓
   take last 20 bytes
        ↓
   Ethereum wallet address (0x...)
```

Going down this chain is easy and fast.
Going back up is the ECDLP. Impossible classically. Shor's solves it.

---

## 10. Why Shor's Breaks This

Your public key is permanently visible on-chain the moment you make a transaction.

Shor's Algorithm looks at your public key and solves:

```
public_key / G = private_key
```

Backward calculation. Impossible classically. Polynomial time on quantum hardware. Every wallet that has ever made a transaction is permanently at risk once a large enough quantum computer exists. The public keys are already recorded on-chain forever.

**This is why post-quantum cryptography exists.**
**This is why Dilithium replaces ECDSA.**

---

## 11. Summary Table

| Concept     | Simple Meaning                                                 |
| ----------- | -------------------------------------------------------------- |
| secp256k1   | The elliptic curve Bitcoin and Ethereum use                    |
| ECDSA       | The signature algorithm that uses secp256k1                    |
| Private key | A random 256-bit number — your secret                          |
| Public key  | private_key × G — safe to share                                |
| G           | Fixed starting point on the curve — hardcoded                  |
| ECDLP       | Going backward from public to private — impossible classically |
| Shor's      | Quantum algorithm that solves ECDLP in polynomial time         |
| Dilithium   | Post-quantum replacement for ECDSA                             |

---

> Next → Dilithium — the quantum resistant signature scheme that replaces everything above.

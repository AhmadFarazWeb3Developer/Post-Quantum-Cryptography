# Diffie-Hellman Key Exchange Protocol

**Year:** 1976  
**Inventors:** Whitfield Diffie and Martin Hellman — Stanford University

---

## Purpose

Allow two parties to agree on a shared secret over a public channel without ever sending the secret itself.

---

## Keys

| Key                         | Type    | Who Knows  |
| --------------------------- | ------- | ---------- |
| `p` — large prime           | Public  | Everyone   |
| `g` — generator             | Public  | Everyone   |
| `a` — Alice's random number | Private | Alice only |
| `b` — Bob's random number   | Private | Bob only   |

---

## Protocol Flow

```
Alice                                        Bob
─────                                        ───
agree on p and g          ←────────────→    agree on p and g

pick secret a                                pick secret b

A = g^a mod p             ────────────→     receives A

receives B                ←────────────     B = g^b mod p

S = B^a mod p                                S = A^b mod p
```

---

## Result

```
Alice computes:  S = B^a mod p = (g^b)^a mod p = g^(ab) mod p
Bob computes:    S = A^b mod p = (g^a)^b mod p = g^(ab) mod p

Both get the same S = g^(ab) mod p  ← shared secret
```

---

## Security

```
Eve sees:    p, g, A, B
Eve needs:   a or b
Problem:     A = g^a mod p  →  finding a = Discrete Logarithm Problem
Result:      Impossible classically for large p
```

---

## Why Shor's Breaks It

Shor's Algorithm solves the Discrete Logarithm Problem in polynomial time on quantum hardware. Eve can now find `a` from `A = g^a mod p`. Shared secret exposed. Protocol broken.

---

## Replaced By

| Classical      | PQC Replacement | Reason                         |
| -------------- | --------------- | ------------------------------ |
| Diffie-Hellman | Kyber (ML-KEM)  | Lattice problem resists Shor's |

---

Great two questions.

---

**What is GCM:**

GCM stands for **Galois Counter Mode.**

It is a mode of operation for AES. AES alone is just a block cipher — it encrypts one fixed block of data. GCM tells AES how to handle real messages.

GCM does two things at once:

```
1. Encrypts your data          → confidentiality
2. Produces an auth tag        → integrity + authentication
```

The auth tag is a small fingerprint of the ciphertext. If anyone tampers with the ciphertext even one bit — decryption fails completely.

```
AES-CBC  → encryption only
AES-GCM  → encryption + authentication together
```

This is why you used `None` as the third parameter — that is the additional authenticated data (AAD). You can pass extra data there that gets authenticated but not encrypted. Like a header.

---

**What is Nonce:**

Nonce stands for **Number Used Once.**

It is a random value that makes every encryption unique even if you encrypt the same message twice with the same key

Without nonce — same key + same message = same ciphertext every time. Attacker spots patterns. Game over.

---

```
Alice encrypts → uses nonce
Alice sends → ciphertext + nonce (together, nonce is public)
Bob decrypts → needs same nonce to reverse the operation
```

In your code you used `os.urandom(12)` — 12 random bytes. In real communication Alice would send this nonce alongside the ciphertext. Bob uses it to decrypt.

---

**The golden rule of nonce:**

Never reuse the same nonce with the same key. Ever. Your code already handles this correctly with `os.urandom(12)` — generates a fresh random nonce every time.

---

**Full picture:**

```
DH/Kyber → shared key (secret, never transmitted)
Nonce → random value (public, transmitted with ciphertext)
AES-GCM → uses both (encrypts + authenticates)
Auth tag → detects tamper (automatically checked on decrypt)

```

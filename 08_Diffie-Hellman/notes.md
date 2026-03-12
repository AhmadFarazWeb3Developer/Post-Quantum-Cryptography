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

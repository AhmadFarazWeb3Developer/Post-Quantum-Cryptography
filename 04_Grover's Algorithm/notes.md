**What is Grover's Algorithm:**

Shor's breaks specific math problems — factoring and discrete logarithm.

Grover's is different. It is a general purpose quantum search algorithm. It speeds up any brute force search.

---

**Simple analogy:**

You lost your key. It is in one of 1 million boxes.

Classical computer — opens boxes one by one. 1,000,000 steps worst case.

Grover's quantum computer — opens all boxes simultaneously using superposition. Finds the key in 1,000 steps.

The speedup is exactly the square root:

```
Classical = N steps
Grover's  = √N steps
```

---

**What does this break:**

Nothing completely. It just weakens everything by halving the security level.

```
AES-128  → Grover's reduces it to 64-bit security → too weak
AES-256  → Grover's reduces it to 128-bit security → still safe
SHA-256  → Grover's reduces it to 128-bit security → still safe
SHA-512  → Grover's reduces it to 256-bit security → very safe
```

The fix is simple — just double your key size. That is it.

---

**Why Grover's cannot destroy lattice crypto:**

Dilithium and Kyber were designed with Grover's already accounted for. Their key sizes are large enough that even after Grover's square root speedup the remaining security is still unbreakable.

```
Dilithium security level → 128-bit after Grover's → safe
Kyber security level     → 128-bit after Grover's → safe
```

NIST specifically required all PQC submissions to maintain 128-bit security even after accounting for Grover's.

---

**Shor's vs Grover's in one table:**

|               | Shor's                            | Grover's                            |
| ------------- | --------------------------------- | ----------------------------------- |
| Type          | Specific attack                   | General search speedup              |
| Effect        | Completely destroys RSA and ECDSA | Halves security level of everything |
| Fix           | Replace the algorithm entirely    | Double the key size                 |
| Threat to PQC | None — lattices have no periods   | Accounted for in key sizes          |
| Urgency       | Existential threat to blockchain  | Manageable, already handled         |

---

**One line:**

> Shor's is a targeted missile that destroys RSA and ECDSA completely. Grover's is background radiation that weakens everything slightly but kills nothing that was designed with it in mind.

That is Grover's. You now have the complete quantum threat picture. Both weapons understood. Now back to Kyber?

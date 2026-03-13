**NTRU = N-Th degree Truncated polynomial Ring Units**

Don't memorize the full name. Just understand what it means.

---

**What a polynomial is — simply:**

```
normal number  →  42
polynomial     →  3x² + 5x + 7
```

A polynomial is just a number with powers of x attached. NTRU does all its math using these polynomials instead of normal numbers.

---

**What a polynomial ring is:**

A ring is just a set of polynomials where you can add and multiply them. But in NTRU there is a rule — the polynomial can only go up to degree N-1. After that it wraps around. Like mod but for polynomials.

```
Normal numbers mod 7:   8 mod 7 = 1   (wraps around)
NTRU polynomials:       x^N = 1       (wraps around at degree N)
```

This wrapping is what makes NTRU compact and fast.

---

**How FALCON uses NTRU — step by step:**

**Step 1 — Key Generation:**

```
Pick two short random polynomials:
f = small coefficients like  1, -1, 0, 1, 0, -1...
g = small coefficients like  0,  1, 1, 0, -1, 0...

Compute public key:
h = g × f^(-1) mod q    ← messy, looks random, hides f and g
```

Private key = f and g (short, clean)
Public key = h (long, messy, hides everything)

---

**Step 2 — Signing:**

```
Hash your message        → get a target point t
Use f and g              → find a short polynomial signature s
                           that is mathematically close to t
Signature = s
```

The word "close" here means the NTRU lattice version of close — the vector is short in the lattice sense.

---

**Step 3 — Verification:**

```
Check two things:
1. s × h mod q is close to the message hash  → correct target
2. s is short enough                          → proves knowledge of private key
```

If both pass — signature valid. Anyone can verify using only the public key h.

---

**Why f and g being short matters:**

```
Short f and g → easy to find short signature s    → private key advantage
Random h      → hard to find short s without f,g  → attacker cannot sign
```

The attacker has h but not f and g. Finding short s from h alone requires solving the NTRU hard problem — which is a specific type of lattice problem with no known quantum solution.

---

**The Gaussian sampling problem:**

When FALCON finds the short signature s — it cannot just pick any short polynomial. It must sample s from a specific probability distribution called a **Gaussian distribution** centered around the target.

```
Gaussian distribution = bell curve shape
Most values close to center
Rare values far from center
```

If the sampling is even slightly biased — signatures start leaking information about f and g. After enough signatures an attacker can reconstruct your private key.

This is why FALCON is dangerous to implement. The Gaussian sampler must be mathematically perfect. One subtle bias in your random number generator — private key exposed.

```
Dilithium  → uses rejection sampling  → if bad randomness, just retry
FALCON     → uses Gaussian sampling   → bad randomness = private key leaked
```

---

**Size comparison explained:**

NTRU signatures are short because:

```
f and g are short polynomials
Short private key → finds short signature → small output
```

RLWE signatures (Dilithium) are larger because:

```
Module lattice structure requires larger polynomials
Larger structure → larger signature → bigger output
```

---

**Complete comparison:**

|                             | Dilithium          | FALCON                      |
| --------------------------- | ------------------ | --------------------------- |
| Lattice type                | Module RLWE        | NTRU                        |
| Signature size              | 2420 bytes         | 666 bytes                   |
| Implementation difficulty   | Moderate           | Hard                        |
| Dangerous if misimplemented | Somewhat           | Very — key exposed          |
| Best use case               | General signing    | Blockchain, compact systems |
| Sampling method             | Rejection sampling | Gaussian sampling           |

---

**One line:**

> FALCON uses short polynomials in an NTRU ring to produce compact signatures. The shortness is the security and the compactness. But Gaussian sampling must be perfect or the private key leaks through the signatures over time.

Now run it. See the signature size. All four algorithms done after this.

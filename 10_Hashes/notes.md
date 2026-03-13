**Each hash family uses different operations:**

```
MD5      → 4 rounds, 64 operations, XOR + AND + OR + NOT + mod 2^32
SHA-1    → 4 rounds, 80 operations, similar to MD5 but stronger mixing
SHA-256  → 64 rounds, bitwise operations + addition mod 2^32 + rotate
SHA-3    → completely different — sponge construction, not rounds based
```

---

**But they all share the same three principles:**

```
1. Modular arithmetic    → destroys magnitude, no reversal
2. Bit mixing operations → XOR, AND, OR, bit rotation, bit shift
3. Multiple rounds       → each round makes reversal exponentially harder
```

More rounds = harder to reverse = more secure.

---

**Why MD5 is broken:**

Only 4 rounds. Not enough mixing. Researchers found two different inputs that produce the same hash — called a **collision.** Security gone.

---

**Why SHA-256 is strong:**

64 rounds of mixing with 8 different state variables interacting with each other simultaneously. Finding a collision requires 2^128 operations — impossible even for quantum computers.

---

**SHA-3 is completely different:**

Does not use rounds at all. Uses a **sponge construction** — absorbs input into a large internal state, squeezes output out. Mathematically completely different from SHA-1 and SHA-2 families.

---

**Simple picture:**

```
MD5/SHA-1/SHA-256  →  compression function + rounds
SHA-3              →  sponge construction
BLAKE2/BLAKE3      →  optimized mixing inspired by SHA-3
```

Same goal — one way fingerprint. Completely different recipes to get there.

---

Now run the tiny hash. Then we build something closer to real SHA-256 with multiple rounds so you feel why rounds matter.

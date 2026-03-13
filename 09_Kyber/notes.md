**Kyber is different:**

One party creates the secret. The other receives it securely.

```
Alice generates keys     → public + private
Bob creates secret       → randomly generates S
Bob encrypts S           → using Alice's public key
Bob sends ciphertext     → to Alice
Alice decrypts           → gets same S
```

Bob decided the secret. Alice received it securely. Alice never contributed to creating it.

---

**Main role of Diffie-Hellman was:**

Both parties contribute to creating the secret together.

```
Alice contributes → a
Bob contributes   → b
Secret            → g^(ab) mod p
```

Neither Alice nor Bob chose the secret alone. It emerged from both of them together. Nobody decided it — it was computed jointly.

---

**Side by side:**

|                    | Diffie-Hellman           | Kyber                     |
| ------------------ | ------------------------ | ------------------------- |
| Who creates secret | Nobody — emerges jointly | Bob creates it            |
| Who chooses secret | Neither party            | Bob                       |
| Alice's role       | Contributes `a`          | Receives encrypted secret |
| Bob's role         | Contributes `b`          | Creates and sends secret  |
| Mechanism          | Math on both sides       | Encrypt and decrypt       |
| Type               | Key Exchange             | Key Encapsulation (KEM)   |
| Hard problem       | Discrete Logarithm       | Lattice LWE               |
| Quantum safe       | No — Shor's breaks it    | Yes — nothing breaks it   |

---

**Why KEM instead of pure exchange:**

DH requires both parties to be online at the same time doing math together simultaneously.

Kyber does not. Bob can encapsulate a secret using Alice's public key even when Alice is offline. Alice decapsulates later. Asynchronous. More practical for real systems.

---

**Real world analogy:**

DH is like two people solving a puzzle together — both must be present, both contribute pieces, solution emerges from cooperation.

Kyber is like Bob putting a secret note in a locked box using Alice's padlock — Alice is not present, Bob creates the note, only Alice's key opens the box.

---

**One line:**

> DH creates a secret jointly through math. Kyber creates a secret unilaterally and delivers it securely through lattice encryption.

Same end result — shared secret. Completely different journey.

# Breaking RSA Example

We are simulating an attack on RSA where the attacker knows the **public key $(e, n)$** and the ciphertext $C$.  
The goal is to recover the **private key $d$** and decrypt the message.

---

## Step 1: Understanding the public key

$n$ is the **modulus**, a number that is the product of two secret primes:

$n = p * q$

Here, $n$ acts as the **dividend** in division terms.

- $e$ is the **encryption exponent**, part of the public key.
- $C$ is the ciphertext that we want to decrypt.

---

## Step 2: Factor the modulus

- To break RSA, the attacker needs `d`, the private key.
- To calculate `d`, they need $\phi$, which requires the prime factors `p` and `q`.

- **Factoring $n$**:

1. The attacker tries dividing $n$ by all integers starting from 2 up to √n.
2. If a number divides $n$ evenly (remainder 0), it is a **divisor**.
3. The corresponding **quotient** is the other prime factor.

- Terms:
- **Dividend**: $n$ (the number being divided)
- **Divisor**: $p$ (first factor found)
- **Quotient**: $q = n / p$ (second factor)

> Once both factors are found, we know $p$ and $q$.

---

## Step 3: Compute $\phi$

$\phi = (p - 1) * (q - 1)$

- $\phi$ is needed to compute the private key $d$.

---

## Step 4: Find the private key $d$

- $d$ satisfies the modular equation:

$(e * d) \  mod \ \phi = 1$

- This means $d$ is the **multiplicative inverse** of $e$ modulo $d$.
- Once $d$ is found, the attacker now has the private key.

---

## Step 5: Decrypt the ciphertext

- Decryption formula:

$M = C^d \ mod \ n$

- This recovers the original plaintext message `M`.

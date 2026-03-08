# RSA (Ron Rivest, Adil Shamir, and Leonard Adelman) for messages and signatures

## 1. Choose two large random private prime number $p \& q$, for max security choose $p\&q$ with equal length $n= p*q$

## 2. Choose randmly encryption exponent $e$, such that $e \& phi = (p-1)(q-1)$ are co-prime (co-prime are those whoe GCD is = 1)

## 3. Now decryption exponent $(e*d) \ mod \ \phi = 1$

## 4. $e$ & $n$ is public key

## 5. $d$ & $n$ is private key

## 6. $p$ & $q$ are no longer needed but keep it private

## 7. Encryption: Cipher = $E(e,n, message)$

$Cipher= message^e \ \% \  n$

## 8. Decryption: message = D(d,n,Cipher)

$message= Cipher^d \  \% \ n$

In real life we do not encrypt message direcly we hash it into signature by any hash function

# Breaking RSA

For breaking RSA we know the public key (e,n) and cipher

for decrypting of cipher the attacker need d

for e \* d mod phi = 1

for finding the d the attacker need phi

for phi the attacker need p and q

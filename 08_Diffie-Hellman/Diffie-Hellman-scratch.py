import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os


# Public values
p = 23
g = 5  # g should be less than p

# Private secrets
a = 6   # Alice
b = 15  # Bob

# Step 1 — compute public values
A = pow(g, a, p)   # Alice sends this to Bob
B = pow(g, b, p)   # Bob sends this to Alice

# Step 2 — compute shared secret
alice_secret = pow(B, a, p)
bob_secret   = pow(A, b, p)

print(alice_secret)  # 2
print(bob_secret)    # 2 — same number, shared secret established


# These secrets are not used directly because they are too small and vary in length.
# They are instead used with AES or other algorithms that require fixed-size keys.
# What are the accepted key sizes for those algorithms?

# For example, if we want to use this key with AES-256,
# we must first convert the Diffie-Hellman generated key into a 256-bit key
# before it can be used by AES-256.


# Stretch to 256 bits using SHA-256
alice_key = hashlib.sha256(str(alice_secret).encode()).digest()  # 32 bytes = 256 bits
bob_key   = hashlib.sha256(str(bob_secret).encode()).digest()  # 32 bytes = 256 bits

# encode() → converts the string into bytes (hash functions only accept byte input)
# digest() → returns the raw 32-byte binary output of the SHA-256 hash

print("Alice 256-bit key:", alice_key.hex())
print("Bob   256-bit key:", bob_key.hex())
print("Length in bits:", len(alice_key) * 8)
print("Match:", alice_key == bob_key)


data = b"a secret message"


key1= alice_key

aesgcm1= AESGCM(key1)

# If you reuse a nonce with the same key — an attacker can XOR two ciphertexts together and cancel out the keystream. Your messages are exposed.
# Nonce being public is fine. Nonce being reused is catastrophic. Your code already handles this correctly.
nonce= os.urandom(12)



cipher=aesgcm1.encrypt(nonce,data,None)
print(cipher.hex())


# Now bob will decrypt with the his secrete key


aes = AESGCM(bob_key)
message=aes.decrypt(nonce,cipher,None)

print(message.decode())




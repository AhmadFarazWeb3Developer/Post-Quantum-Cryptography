from pqcrypto.kem import ml_kem_768
from  cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib
import os
# Step 1 — Alice generates keys
public_key, private_key = ml_kem_768.generate_keypair()

# Step 2 — Bob encapsulates secret using Alice's public key
ciphertext, bob_secret = ml_kem_768.encrypt(public_key)

# Step 3 — Alice decapsulates to get same secret
alice_secret = ml_kem_768.decrypt(private_key, ciphertext)

print("Bob secret:  ", bob_secret.hex())
print("Alice secret:", alice_secret.hex())
print("Match:       ", bob_secret == alice_secret)


#  Learning      → ml_kem_768
#  Production    → ml_kem_768 or ml_kem_1024
#  Maximum speed → ml_kem_512


# Step 2 — Stretch to 256 bits
alice_key = hashlib.sha256(alice_secret).digest()
bob_key   = hashlib.sha256(bob_secret).digest()


message = b"Ahmad Faraz - PQC Journey"


aesgcm1=AESGCM(alice_key)
nonce= os.urandom(12)


encrypted = aesgcm1.encrypt(nonce,message,None)
print("Encrypted : ",encrypted.hex())

aesgcm2=AESGCM(bob_key)

decrypted=aesgcm2.decrypt(nonce,encrypted,None)

print("decrypted : ",decrypted)


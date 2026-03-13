from pqcrypto.sign import sphincs_sha2_128f_simple as sphincs

# sphincs  →  the algorithm name
# sha2     →  uses SHA-256 as the hash function underneath
# 128      →  128-bit security level
# f        →  fast variant (larger signature, faster signing)
# simple   →  simpler internal construction (vs robust variant)

# f → fast    → signs faster, bigger signature
# s → small   → signs slower, smaller signature

public_key,private_key=sphincs.generate_keypair()


message = b"Ahmad Faraz - PQC Journey"

signature=sphincs.sign(private_key,public_key)


verify=sphincs.verify(public_key,message,signature)
print("Valid:", verify)

# Tamper test
result = sphincs.verify(public_key, b"HACKED", signature)
print("Tampered:", result)

# See how big the signature is
print("Signature size:", len(signature), "bytes")
print("Compare Dilithium: ~2420 bytes")
print("Compare ECDSA:     ~64 bytes")
from pqcrypto.sign import falcon_512

# Generate keys
public_key, private_key = falcon_512.generate_keypair()

# Sign
message = b"Ahmad Faraz - PQC Journey"
signature = falcon_512.sign(private_key, message)

# Verify
result = falcon_512.verify(public_key, message, signature)
print("Valid:", result)

# Tamper test
result = falcon_512.verify(public_key, b"HACKED", signature)
print("Tampered:", result)

# Size comparison
print("\nSignature sizes:")
print("FALCON:    ", len(signature), "bytes")
print("Dilithium:  ~2420 bytes")
print("SPHINCS+:   ~17000 bytes")
print("ECDSA:      ~64 bytes")
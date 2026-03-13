from pqcrypto.sign import ml_dsa_44

public_key, private_key=ml_dsa_44.generate_keypair()

message= b"Ahmad Faraz - PQC Journey"

signature= ml_dsa_44.sign(private_key,message)

result = ml_dsa_44.verify(public_key, message, signature)
print("Original message:", result)

# Verify tampered
result = ml_dsa_44.verify(public_key, b"HACKED MESSAGE", signature)
print("Tampered message:", result)


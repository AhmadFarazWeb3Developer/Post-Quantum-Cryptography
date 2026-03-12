from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.exceptions import InvalidSignature

private_key= Ed25519PrivateKey.generate()
public_key=private_key.public_key()

message= b"Ahmad Faraz - PQC Journey"

signature=private_key.sign(message)

fake_message = b"Ahmad Faraz - PQC Journey HACKED"

try:
    public_key.verify(signature, fake_message)
    print("Valid")
except InvalidSignature:
    print("FAILED — message was tampered")
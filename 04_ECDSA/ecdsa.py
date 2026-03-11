from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes


private_key=ec.generate_private_key(ec.SECP256K1())
print(private_key)
public_key=private_key.public_key()
print(public_key)


message= b"Ahmad Faraz"
signature=private_key.sign(message,ec.ECDSA(hashes.SHA256()))
print(signature)



verify=public_key.verify(signature,message,ec.ECDSA(hashes.SHA256()))
print("Verified!")
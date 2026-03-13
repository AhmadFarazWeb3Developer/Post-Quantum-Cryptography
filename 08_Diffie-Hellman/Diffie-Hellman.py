# import cryptography  # brings everything
# cryptography.hazmat.primitives.asymmetric.dh.generate_parameters()  # long path every time
# from x import y brings only what you need:

from cryptography.hazmat.primitives.asymmetric.dh import generate_parameters
from cryptography.hazmat.primitives import serialization
import hashlib


# p = random number of 512 size
# g = 2 

parameters=generate_parameters(generator=2,key_size=512)


alice_private = parameters.generate_private_key() #  a
alice_public  = alice_private.public_key() #  A = g^a mod p 


bob_private = parameters.generate_private_key()  # b
bob_public  = bob_private.public_key()   # B = g^b mod p


alice_secret=alice_private.exchange(bob_public) # S = B^a mod p   
bob_secret=bob_private.exchange(alice_public) #  S = A^b mod p


alice_key=hashlib.sha256(alice_secret).digest()
bob_key=hashlib.sha256(bob_secret).digest()

print(alice_key.hex())
print(bob_key.hex())
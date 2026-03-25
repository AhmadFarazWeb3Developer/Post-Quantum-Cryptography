import json
from pqcrypto.sign import falcon_512 as falcon

# Keys generation
public_key, private_key = falcon.generate_keypair()

print(public_key.hex())
print(private_key.hex())

keys={
    'public_key':public_key.hex(),
    'private_key':private_key.hex()
}
with open ("14_Account-abstraction/encryption/keys.json",'w')as file:
    file.write(json.dumps(keys))


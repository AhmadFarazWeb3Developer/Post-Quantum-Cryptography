import json
import hashlib
from pqcrypto.sign import falcon_512 as falcon


# Keys generation
public_key, private_key = falcon.generate_keypair()



# Read deployed address
with open("14_Account-abstraction/deployment/deployedAddress.json", "r") as file:
    deployment = json.load(file)

simpleAccount = deployment["simpleAccount"]

userOperation = {
  "sender": simpleAccount,
  "nonce": 1,
  "initCode": "0x",
  "callData": "0x",
  "accountGasLimits":
    "0x0000000000000000000000000000000000000000000000000000000000000000",
  "preVerificationGas": 50000,
  "gasFees": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "paymasterAndData": "0x",
  "signature": "0x", 
}


userOpHash =hashlib.sha256(json.dumps(userOperation).encode()).digest()

signature=falcon.sign(private_key,userOpHash)
print(f"Signature length: {len(signature)} bytes")
print(f"Signature hex: {signature.hex()}")
print(f"UserOp: {userOperation}")

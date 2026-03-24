import json
from Crypto.Hash import keccak
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

keccak_hash =keccak.new(digest_bits=256)
keccak_hash.update(json.dumps(userOperation).encode())
userOpHash=keccak_hash.digest()


print(f"UserOp: {keccak_hash.hexdigest()}")


commitment_hash = keccak.new(digest_bits=256)
commitment_hash.update(userOpHash + public_key)
commitment = commitment_hash.digest()


TARGET = 666

signature=falcon.sign(private_key,userOpHash)

# Must re-sign if the signature length exceeds 666 bytes, until valid length is 666 bytes of less
while True:
    signature = falcon.sign(private_key, userOpHash)
    
    if len(signature) <= TARGET:
        signature = signature + b'\x00' * (TARGET - len(signature))
        break
    
final_signature = commitment + signature

userOperation["signature"] = "0x" + final_signature.hex()


print(f"Signature hex: {signature.hex()}")
print(f"Signature length: {len(signature)} bytes")
print(f"Signature length: {len(final_signature)} bytes")
print(f"UserOp: {userOperation}")

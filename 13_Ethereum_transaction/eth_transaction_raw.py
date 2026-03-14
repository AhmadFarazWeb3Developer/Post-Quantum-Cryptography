
from eth_account import Account
from web3 import Web3

# Raw transaction fields
transaction = {
    'nonce': 0,
    'gasPrice': 20000000000,
    'gas': 21000,
    'to': '0x742d35Cc6634C0532925a3b8D4C9C3D5eA6A2Ce1',
    'value': 1000000000000000000,
    'data': b'',
    'chainId': 11155111
}

# Sign it
private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
signed = Account.sign_transaction(transaction, private_key)

# What gets signed
print("Hash that ECDSA signed:", signed.hash.hex())
print("Signature r:", hex(signed.r))
print("Signature s:", hex(signed.s))
print("Signature v:", signed.v)
print("Full raw transaction:", signed.rawTransaction.hex())


# **What each thing means simply:**

# ```
# signed.hash  → the Keccak-256 hash of RLP encoded transaction
#                THIS is what ECDSA signs — not the transaction itself

# signed.r     → first part of ECDSA signature
# signed.s     → second part of ECDSA signature  
# signed.v     → recovery id — helps recover public key from signature

# rawTransaction → everything packed together, ready to broadcast
# ```

# ---

# **RLP encoding simply:**

# RLP is just Ethereum's way of packing multiple fields into one bytes string. Like JSON but binary and compact.

# ```
# {nonce, gasPrice, gas, to, value, data, chainId}
#              ↓ RLP encode
#     0xf86c808504a817c800...  (raw bytes)
#              ↓ Keccak-256
#     0x7f4a...  (32 byte hash)
#              ↓ ECDSA sign
#     r, s, v
# ```

# Run it. Tell me what you get.
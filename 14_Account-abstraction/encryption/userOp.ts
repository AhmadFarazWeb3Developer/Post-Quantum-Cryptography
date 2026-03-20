const userOperation = {
  sender: simpleAccount,
  nonce: 1,
  initCode: "0x",
  callData: "0x",
  accountGasLimits:
    "0x0000000000000000000000000000000000000000000000000000000000000000",
  preVerificationGas: 50000n,
  gasFees: "0x0000000000000000000000000000000000000000000000000000000000000000",
  paymasterAndData: "0x",
  signature: "0x", // Will fill after signing
};

privateKey.sign(privateKey, userOperation);

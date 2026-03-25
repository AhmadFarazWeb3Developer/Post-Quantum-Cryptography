import { ethers } from "ethers";
import simpleAccountArtifact from "../artifacts/contracts/accounts/SimpleAccount.sol/SimpleAccount.json" with{type:"json"};
import deployment from "../deployment/deployedAddress.json" with{type:"json"};
import keys from "../encryption/keys.json" with{type:"json"};
import userOperaction from "../encryption/operations.json" with{type:"json"}

import { Contract } from "ethers";

const simpleAccountAbi = simpleAccountArtifact.abi;
const simpleAccountAddress = deployment.simpleAccount;

const userOp=userOperaction.userOp
const userOpHash= ethers.getBytes (userOperaction.userOpHash)


const provider = new ethers.JsonRpcProvider("http://127.0.0.1:8545/");
const signer = await provider.getSigner();

const simpleAccount = new Contract(
  simpleAccountAddress,
  simpleAccountAbi,
  signer,
);

const falconPublicKey = ethers.getBytes(`0x${keys.public_key}`);


const setFalconPublicKey = await simpleAccount.setFalconPublicKey(
  falconPublicKey,
);
await setFalconPublicKey.wait();

const validationResult= await simpleAccount.testValidateSignature(userOp,userOpHash);

if (validationResult === 0n) {
  console.log("Signature Validation Succeeded!");
} else {
  console.log("Signature Validation Failed.");
}






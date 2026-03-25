import { ethers } from "ethers";
import simpleAccountArtifact from "../artifacts/contracts/accounts/SimpleAccount.sol/SimpleAccount.json";
import deployment from "../deployment/deployedAddress.json";
import keys from "../encryption/keys.json";
import { Contract } from "ethers";

const simpleAccountAbi = simpleAccountArtifact.abi;
const simpleAccountAddress = deployment.simpleAccount;
const owner = deployment.eoa_public_key;

const provider = new ethers.JsonRpcProvider("http://127.0.0.1:8545/");
const signer = await provider.getSigner();

const simpleAccount = new Contract(
  simpleAccountAddress,
  simpleAccountAbi,
  signer,
);

const falconPublicKey = ethers.getBytes(keys.public_key);

const setOwnerTx = await simpleAccount.initialize(owner);
await setOwnerTx.wait();

const setFalconPublicKey = await simpleAccount.setFalconPublicKey(
  falconPublicKey,
);

await setFalconPublicKey.wait();

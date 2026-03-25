import hre from "hardhat";
import fs from "fs";

const { network } = hre;

const { ethers } = await network.connect({ network: "localhost" });

const deployContracts = async () => {
  //As we cannot deploy the EntryPoint locally so choossing dummy address for it
  // Real EntryPoint is too large (30KB) to deploy on localhost
  // Use placeholder for contract initialization only

  const [owner] = await ethers.getSigners();

  const entryPoint = "0x0000000000000000000000000000000000000001";

  const SimpleAccount = await ethers.getContractFactory("SimpleAccount");

  const simpleAccount = await SimpleAccount.deploy(entryPoint);

  await simpleAccount.waitForDeployment();

  console.log("SimpleAccount deployed at:", simpleAccount.target);

  const folder = "deployment";
  if (!fs.existsSync(folder)) {
    fs.mkdirSync(folder);
  }

  // Save deployed address
  fs.writeFileSync(
    `${folder}/deployedAddress.json`,
    JSON.stringify(
      {
        simpleAccount: simpleAccount.target,
        eoa_public_key: owner.address,
      },
      null,
      2,
    ),
  );

  // NOT deploying SimpleAccountFactory because:
  // - Factory constructor calls _entryPoint.senderCreator()
  // - Fails on dummy address (no code to call)
  // - Factory not needed for signature validation testing
  // - Will deploy on mainnet/testnet where real EntryPoint exists
};

deployContracts().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

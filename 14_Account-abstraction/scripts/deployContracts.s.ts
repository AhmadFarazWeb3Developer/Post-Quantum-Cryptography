import hre from "hardhat";

const { network } = hre;

const { ethers } = await network.connect({ network: "localhost" });

const deployContracts = async () => {
  const SimpleAccount = await ethers.getContractFactory("SimpleAccount");
  const EntryPoint = await ethers.getContractFactory("EntryPoint");
  const SimpleAccountFactory = await ethers.getContractFactory(
    "SimpleAccountFactory",
  );

  const entryPoint = await EntryPoint.deploy();
  await entryPoint.waitForDeployment();

  const simpleAccount = await SimpleAccount.deploy(entryPoint.target);
  await simpleAccount.waitForDeployment();
  const simpleAccountFactory = await SimpleAccountFactory.deploy(
    entryPoint.target,
  );
  await simpleAccountFactory.waitForDeployment();

  console.log("EntryPoint deployed at:", entryPoint.target);
  console.log("SimpleAccountFactory deployed at:", simpleAccountFactory.target);
  console.log("SimpleAccount deployed at:", simpleAccount.target);
};

deployContracts().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("FLASH TRC20", function () {
  const TOTAL = ethers.parseUnits("1000000000", 6);
  let token, deployer, a, b;

  beforeEach(async function () {
    [deployer, a, b] = await ethers.getSigners();
    const FLASH = await ethers.getContractFactory("FLASH");
    token = await FLASH.deploy();
    await token.waitForDeployment();
  });

  it("has the expected fixed supply", async function () {
    expect(await token.totalSupply()).to.equal(TOTAL);
    expect(await token.balanceOf(deployer.address)).to.equal(TOTAL);
  });

  it("transfers without changing total supply", async function () {
    const before = await token.totalSupply();
    await token.connect(deployer).transfer(b.address, ethers.parseUnits("1000", 6));
    expect(await token.balanceOf(b.address)).to.equal(ethers.parseUnits("1000", 6));
    expect(await token.totalSupply()).to.equal(before);
  });

  it("has no external mint function", async function () {
    expect(token.mint).to.equal(undefined);
  });

  it("has no privileged admin surface", async function () {
    const forbidden = [
      "mint", "burn", "pause", "unpause", "freeze", "blacklist",
      "addBlacklist", "removeBlacklist", "upgrade", "setBlacklist",
      "transferOwnership", "renounceOwnership", "owner"
    ];
    for (const fn of forbidden) {
      expect(token[fn], `unexpected function: ${fn}`).to.equal(undefined);
    }
  });

  it("supports approval and transferFrom", async function () {
    await token.connect(deployer).approve(a.address, ethers.parseUnits("500", 6));
    await token.connect(a).transferFrom(
      deployer.address,
      b.address,
      ethers.parseUnits("500", 6)
    );
    expect(await token.balanceOf(b.address)).to.equal(ethers.parseUnits("500", 6));
  });
});

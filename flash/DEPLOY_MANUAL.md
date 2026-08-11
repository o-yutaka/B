# FLASH Shasta — TronLink checklist

## 0. Prepare

- TronLink installed
- Network: TRON Shasta Testnet
- Test TRX available

## 1. Compile

Open the official TRON IDE and load `flash/contracts/FLASH.sol`.

Use:

- Solidity: `0.8.19`
- Optimization: enabled
- Runs: `200`

Compile successfully and select contract `FLASH`.

## 2. Deploy

Use the injected TronLink environment / Shasta network.

Constructor arguments: none.

Click Deploy and approve the transaction in TronLink.

Record:

- Contract Address
- Deployment transaction hash

## 3. Verify

Open Shasta TRONSCAN and verify the exact source/compiler configuration used for deployment.

## 4. Post-deploy checks

Confirm on-chain:

- `name()` = `FLASH`
- `symbol()` = `FLASH`
- `decimals()` = `6`
- `totalSupply()` = `1,000,000,000 * 10^6`
- deployer balance initially equals total supply
- no privileged mint/admin interface exists

## Secret handling

Never paste a private key or mnemonic into chat, GitHub, or this repository. Browser signing remains entirely under the wallet owner’s control.

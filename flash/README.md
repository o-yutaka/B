# FLASH — TRON Shasta

Independent fixed-supply TRC20 experiment.

## Token spec

- Name: FLASH
- Symbol: FLASH
- Decimals: 6
- Initial / maximum supply: 1,000,000,000 FLASH
- Mint after deployment: none
- Burn: none
- Transfer tax / fee: 0%
- Pause / blacklist / upgrade / owner-admin: none

## Security boundary

Browser-wallet signing is user-side. Never commit private keys, mnemonics, or `.env` files.

## Local checks

The source-level design is intended to satisfy:

- total supply equals 1,000,000,000 FLASH
- deployer receives the complete initial supply
- normal transfers do not change total supply
- no external mint or privileged admin functions exist
- approve/transferFrom remain standard ERC20 behavior

## Shasta deployment

1. Install TronLink and switch to the TRON Shasta Testnet.
2. Obtain test TRX from the official Shasta faucet.
3. Compile `flash/contracts/FLASH.sol` with a TRON-compatible Solidity environment (for example TRON IDE) using Solidity 0.8.19 and optimizer runs 200.
4. Deploy `FLASH` with no constructor arguments.
5. Sign the deployment in TronLink.
6. Record the resulting Contract Address and deployment transaction hash.
7. Verify the exact deployed source on Shasta TRONSCAN.

No private key is required in this repository to perform the browser-wallet deployment.

## Mainnet / DEX gate

Do not treat Shasta deployment as production readiness. Mainnet and any DEX liquidity step require a separate review of:

- contract bytecode and source match
- authority surface
- metadata
- allocation and custody
- liquidity design
- legal / tax requirements for the intended jurisdictions

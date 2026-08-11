// User-side signing is required. Do not place private keys in this repository.
// This script prepares transaction parameters only; actual deployment must be
// signed by TronLink/TronIDE in the user's browser.
const fs = require('fs');
const path = require('path');

const out = {
  network: 'shasta',
  contract: 'FLASH',
  source: 'flash/contracts/FLASH_tronide.sol',
  signing: 'TronLink user confirmation',
  next: [
    'Compile exact source with TronIDE using Solidity 0.8.19, optimizer enabled, runs 200',
    'Deploy with TronLink on Shasta',
    'Record deployment transaction hash and contract address',
    'Verify exact source on Shasta TRONSCAN'
  ]
};

fs.mkdirSync(path.join(__dirname, '..', 'deployments'), { recursive: true });
fs.writeFileSync(
  path.join(__dirname, '..', 'deployments', 'shasta-deploy-checklist.json'),
  JSON.stringify(out, null, 2) + '\n'
);
console.log(JSON.stringify(out, null, 2));

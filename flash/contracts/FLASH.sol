// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/// @title FLASH
/// @notice Independent TRC20 token for the FLASH experiment.
/// Fixed supply; no mint/burn/pause/blacklist/upgrade/owner-admin controls.
/// This contract is independent from any existing USDT-TRC20 token.
contract FLASH is ERC20 {
    uint8 private constant _DECIMALS = 6;
    uint256 private constant _TOTAL_SUPPLY = 1_000_000_000 * 10 ** _DECIMALS;

    constructor() ERC20("FLASH", "FLASH") {
        _mint(msg.sender, _TOTAL_SUPPLY);
    }

    function decimals() public view virtual override returns (uint8) {
        return _DECIMALS;
    }
}

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import '@eigenphi/mev-shield/contracts/Validator.sol';
contract FlashSynapse is Validator {
    function executeLoan() external payable {
        require(validateTx(tx.origin), 'MEV protection');
    }
}

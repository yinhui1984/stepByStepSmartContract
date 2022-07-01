// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Calculator {

    function add(int a, int b) public pure returns (int)  {
        return a + b;
    }

    function subtract(int a, int b) public pure returns (int) {
        return a - b;
    }
}
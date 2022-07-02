const fs = require('fs');
const Web3 = require('web3');
const web3 = new Web3('http://127.0.0.1:8545');

const bytecode = fs.readFileSync('../build/Calculator.bin').toString();
const abi = JSON.parse(fs.readFileSync('../build/Calculator.abi').toString());

(async function () {
    const accounts = await web3.eth.getAccounts();

    const calculator = new web3.eth.Contract(abi);

    calculator.deploy({
        data: bytecode
    }).send({
        from: accounts[0],
    }).then((deployment) => {
        console.log('Contract was deployed at the following address:');
        console.log(deployment.options.address);
    }).catch((err) => {
        console.error(err);
    });
})();





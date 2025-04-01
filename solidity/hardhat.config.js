require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.20",
  networks: {
    hardhat: { // Rede local integrada
      chainId: 31337, // ID padrão do Hardhat
    }
  }
};

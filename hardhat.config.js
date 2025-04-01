require('@nomiclabs/hardhat-ethers');
require('dotenv').config();

module.exports = {
  solidity: "0.8.19", // Versão do Solidity que você está utilizando
  networks: {
    polygon: {
      url: "https://polygon-rpc.com", // Usando o RPC da Polygon Mainnet
      accounts: [`0x${process.env.PRIVATE_KEY}`], // A chave privada é obtida do .env
    },
  },
};


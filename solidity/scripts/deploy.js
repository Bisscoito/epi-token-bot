const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  // 1. Configuração inicial
  console.log("🚀 Iniciando deploy do LiquidityPool...");
  
  // 2. Carrega variáveis de ambiente
  require("dotenv").config();
  const tokenAddress = process.env.TOKEN_ADDRESS;
  
  if (!tokenAddress) {
    throw new Error("❌ TOKEN_ADDRESS não definido no .env");
  }

  // 3. Obtém o contrato
  const LiquidityPool = await hre.ethers.getContractFactory("LiquidityPool");
  
  // 4. Faz o deploy
  console.log("📡 Conectando à blockchain...");
  const pool = await LiquidityPool.deploy(tokenAddress);
  console.log("⏳ Aguardando confirmação...");
  await pool.deployed();
  
  // 5. Salva o endereço
  const envPath = path.join(__dirname, "..", ".env");
  const envContent = fs.existsSync(envPath) ? fs.readFileSync(envPath, "utf8") : "";
  
  // Atualiza apenas as variáveis necessárias
  const updatedEnv = envContent
    .replace(/CONTRACT_ADDRESS=.*\n?/, "")
    .replace(/TOKEN_ADDRESS=.*\n?/, "")
    + `CONTRACT_ADDRESS=${pool.address}\nTOKEN_ADDRESS=${tokenAddress}\n`;
  
  fs.writeFileSync(envPath, updatedEnv.trim());

  console.log("✅ Sucesso! Contrato deployado em:", pool.address);
  console.log("📝 Arquivo .env atualizado:");
  console.log(`CONTRACT_ADDRESS=${pool.address}`);
  console.log(`TOKEN_ADDRESS=${tokenAddress}`);
}

main().catch((error) => {
  console.error("❌ Falha no deploy:", error);
  process.exitCode = 1;
});

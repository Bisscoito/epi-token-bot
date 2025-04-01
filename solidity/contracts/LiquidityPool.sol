// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract LiquidityPool is ReentrancyGuard {
    // 1. Estrutura de dados aprimorada
    struct Deposit {
        uint256 amount;
        uint256 timestamp;
    }
    
    mapping(address => Deposit[]) public userDeposits;
    mapping(address => uint256) public totalUserBalance;
    uint256 public totalLiquidity;
    address public immutable tokenAddress; // Endereço do token ERC20 (ex: USDC)
    
    // 2. Eventos detalhados
    event Deposited(address indexed user, uint256 amount, uint256 newTotalLiquidity);
    event Withdrawn(address indexed user, uint256 amount, uint256 newTotalLiquidity);
    event EmergencyWithdraw(address indexed admin, uint256 amount);

    // 3. Modificador para o dono (opcional)
    address public owner;
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    // 4. Inicialização com token ERC20
    constructor(address _tokenAddress) {
        tokenAddress = _tokenAddress;
        owner = msg.sender;
    }

    // 5. Depósito em MATIC e token simultaneamente
    function deposit(uint256 tokenAmount) external payable nonReentrant {
        require(msg.value > 0 || tokenAmount > 0, "Must deposit something");
        
        if (msg.value > 0) {
            userDeposits[msg.sender].push(Deposit(msg.value, block.timestamp));
            totalUserBalance[msg.sender] += msg.value;
            totalLiquidity += msg.value;
        }
        
        if (tokenAmount > 0) {
            IERC20 token = IERC20(tokenAddress);
            require(token.transferFrom(msg.sender, address(this), tokenAmount), "Token transfer failed");
            // Lógica adicional para tokens aqui
        }
        
        emit Deposited(msg.sender, msg.value, totalLiquidity);
    }

    // 6. Saque com período de lock (opcional)
    function withdraw(uint256 amount) external nonReentrant {
        require(amount <= totalUserBalance[msg.sender], "Insufficient balance");
        require(checkWithdrawAvailability(msg.sender, amount), "Funds locked");
        
        totalUserBalance[msg.sender] -= amount;
        totalLiquidity -= amount;
        
        (bool sent,) = msg.sender.call{value: amount}("");
        require(sent, "Failed to send MATIC");
        
        emit Withdrawn(msg.sender, amount, totalLiquidity);
    }

    // 7. Verificação de disponibilidade para saque
    function checkWithdrawAvailability(address user, uint256 amount) public view returns (bool) {
        // Exemplo: 50% pode sacar imediatamente, 50% após 7 dias
        uint256 availableAmount;
        for (uint i = 0; i < userDeposits[user].length; i++) {
            if (block.timestamp >= userDeposits[user][i].timestamp + 7 days) {
                availableAmount += userDeposits[user][i].amount;
            } else {
                availableAmount += userDeposits[user][i].amount / 2;
            }
        }
        return amount <= availableAmount;
    }

    // 8. Função de emergência (apenas owner)
    function emergencyWithdraw() external onlyOwner {
        uint256 balance = address(this).balance;
        payable(owner).transfer(balance);
        emit EmergencyWithdraw(owner, balance);
    }
}

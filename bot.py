import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from web3 import Web3
import os
import json

# Configuração
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Conexão com Polygon
w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
CONTRACT_ADDRESS = '0xSeuContrato'  # Substitua pelo seu contrato
PRIVATE_KEY = os.getenv('PRIVATE_KEY')  # Chave da carteira do bot

# ABI do Contrato (simplificado)
CONTRACT_ABI = json.loads('''[
    {
        "inputs": [
            {"name": "amount", "type": "uint256"}
        ],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]''')

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Teclado
def deposit_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🔗 Ver no PolygonScan", url=f"https://polygonscan.com/address/{CONTRACT_ADDRESS}")
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "💰 *Depósito Real na Polygon* 💰\n\n"
        "Envie o valor em MATIC que deseja depositar:",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: True)
def handle_deposit(message):
    try:
        amount = float(message.text)
        wei_amount = w3.to_wei(amount, 'ether')
        
        # Prepara transação
        tx = contract.functions.deposit(wei_amount).build_transaction({
            'chainId': 137,
            'gas': 200000,
            'gasPrice': w3.to_wei('50', 'gwei'),
            'nonce': w3.eth.get_transaction_count(w3.eth.account.from_key(PRIVATE_KEY).address),
            'value': wei_amount
        })
        
        # Assina e envia
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        bot.send_message(
            message.chat.id,
            f"✅ *{amount} MATIC depositados!*\n"
            f"Tx Hash: `{tx_hash.hex()}`",
            parse_mode="Markdown",
            reply_markup=deposit_keyboard()
        )
    
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro: {str(e)}")

if __name__ == '__main__':
    bot.polling()
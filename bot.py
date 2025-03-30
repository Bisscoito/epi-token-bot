import os
import telebot
from telebot import types

bot = telebot.TeleBot(os.environ['EPI_TOKEN'])

# Menu Principal
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton('👤 Cadastro'),
        types.KeyboardButton('📊 Saldo'),
        types.KeyboardButton('🔗 Código Indicação'),
        types.KeyboardButton('⛏️ Abrir Minerador'),
        types.KeyboardButton('💸 Saque'),
        types.KeyboardButton('ℹ️ Ajuda')
    )
    return markup

# Handlers
@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    bot.send_message(message.chat.id, "🛠️ *MobileCoin Miner* 🛠️\nEscolha uma opção:", 
                   reply_markup=main_menu(), parse_mode='Markdown')

@bot.message_handler(func=lambda msg: msg.text == '⛏️ Abrir Minerador')
def start_miner(message):
    bot.send_message(message.chat.id, "🔗 [Clique para acessar o minerador](https://github.com/Bisscoito/mobilecoin-miner)",
                   parse_mode='Markdown')

@bot.message_handler(func=lambda msg: msg.text == '👤 Cadastro')
def register(message):
    msg = bot.send_message(message.chat.id, "📧 Digite seu e-mail para cadastro:")
    bot.register_next_step_handler(msg, save_email)

def save_email(message):
    # Aqui você pode integrar com um banco de dados
    bot.send_message(message.chat.id, f"✅ Cadastrado: {message.text}")

@bot.message_handler(func=lambda msg: msg.text == '📊 Saldo')
def show_balance(message):
    bot.send_message(message.chat.id, "💰 *Saldo atual:* 100 MOB", parse_mode='Markdown')

if __name__ == "__main__":
    print("🤖 Bot MobileCoin Miner Ativo!")
    bot.infinity_polling()

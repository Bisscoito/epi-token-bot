import os
from dotenv import load_dotenv
import telebot

load_dotenv()
TOKEN = os.getenv("EPI_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot funcionando! Token está seguro.")

if __name__ == "__main__":
    print("Bot rodando...")
    bot.infinity_polling()

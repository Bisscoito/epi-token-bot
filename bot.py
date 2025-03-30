from telebot import types
import re

# Dicionário temporário (substitua por banco de dados depois)
user_data = {}

# Handler para o comando Ajuda
@bot.message_handler(func=lambda msg: msg.text == 'ℹ️ Ajuda')
def show_help(message):
    help_text = (
        "🆘 *Ajuda*\n\n"
        "👤 Cadastro: Registre-se no sistema\n"
        "⛏️ Minerador: Acesse o minerador MobileCoin\n"
        "📊 Saldo: Consulte seu saldo\n"
        "💸 Saque: Solicite saque de MOB"
    )
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

# Handler para Cadastro
@bot.message_handler(func=lambda msg: msg.text == '👤 Cadastro')
def start_registration(message):
    if str(message.chat.id) in user_data:
        bot.send_message(message.chat.id, "✅ Você já está cadastrado!")
        return
    
    msg = bot.send_message(
        message.chat.id,
        "📝 *Cadastro*\n\nPor favor, digite seu e-mail válido:",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_email_step)

def process_email_step(message):
    # Se usuário desistir e clicar em Ajuda
    if message.text == 'ℹ️ Ajuda':
        show_help(message)
        return
    
    # Validação básica de e-mail
    if not re.match(r"[^@]+@[^@]+\.[^@]+", message.text):
        msg = bot.send_message(
            message.chat.id,
            "❌ E-mail inválido. Por favor, digite novamente:"
        )
        bot.register_next_step_handler(msg, process_email_step)
        return
    
    # Salva os dados temporariamente
    user_data[str(message.chat.id)] = {
        'email': message.text,
        'telegram_name': message.from_user.first_name,
        'wallet': None  # Será preenchido depois
    }
    
    # Pede a carteira MOB
    msg = bot.send_message(
        message.chat.id,
        "🔑 Agora digite seu endereço da carteira MobileCoin:",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_wallet_step)

def process_wallet_step(message):
    # Validação básica de carteira (adaptar para MOB)
    if len(message.text) < 10:  # Exemplo simples
        msg = bot.send_message(
            message.chat.id,
            "❌ Carteira inválida. Digite novamente:"
        )
        bot.register_next_step_handler(msg, process_wallet_step)
        return
    
    # Completa o cadastro
    user_data[str(message.chat.id)]['wallet'] = message.text
    
    bot.send_message(
        message.chat.id,
        f"✅ *Cadastro completo!*\n\n"
        f"👤 Nome: {user_data[str(message.chat.id)]['telegram_name']}\n"
        f"📧 E-mail: {user_data[str(message.chat.id)]['email']}\n"
        f"💰 Carteira: `{user_data[str(message.chat.id)]['wallet']}`",
        parse_mode='Markdown'
    )

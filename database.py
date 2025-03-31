@bot.message_handler(func=lambda msg: msg.text == '👤 Cadastro')
def start_registration(message):
    user = get_user(str(message.chat.id))
    if user:
        bot.send_message(message.chat.id, "✅ Você já está cadastrado!")
        return
    
    msg = bot.send_message(
        message.chat.id,
        "📝 *Cadastro*\n\nPor favor, digite seu e-mail válido:",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_email_step)

def process_email_step(message):
    if message.text == 'ℹ️ Ajuda':
        show_help(message)
        return
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", message.text):
        msg = bot.send_message(
            message.chat.id,
            "❌ E-mail inválido. Por favor, digite novamente:"
        )
        bot.register_next_step_handler(msg, process_email_step)
        return
    
    msg = bot.send_message(
        message.chat.id,
        "🔑 Agora digite seu endereço da carteira MobileCoin:",
        parse_mode='Markdown'
    )
    # Armazena temporariamente o email
    bot.register_next_step_handler(
        msg, 
        lambda m: process_wallet_step(m, message.text, message.from_user.first_name)
    )

def process_wallet_step(message, email, telegram_name):
    if len(message.text) < 10:  # Validação básica
        msg = bot.send_message(
            message.chat.id,
            "❌ Carteira inválida. Digite novamente:"
        )
        bot.register_next_step_handler(
            msg, 
            lambda m: process_wallet_step(m, email, telegram_name)
        )
        return
    
    if save_user(
        user_id=str(message.chat.id),
        email=email,
        telegram_name=telegram_name,
        wallet_address=message.text
    ):
        bot.send_message(
            message.chat.id,
            f"✅ *Cadastro completo!*\n\n"
            f"👤 Nome: {telegram_name}\n"
            f"📧 E-mail: {email}\n"
            f"💰 Carteira: `{message.text}`",
            parse_mode='Markdown'
        )
    else:
        bot.send_message(
            message.chat.id,
            "❌ Erro ao salvar cadastro. Tente novamente mais tarde."
        )

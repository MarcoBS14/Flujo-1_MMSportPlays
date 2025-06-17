import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Cargar el token desde .env o Railway
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# MENSAJE /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("1. Información sobre el grupo premium", callback_data="info_premium")],
        [InlineKeyboardButton("2. Preguntas frecuentes", callback_data="faq")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("¡Hola! 👋 ¿Cómo puedo ayudarte hoy?", reply_markup=reply_markup)

# RESPUESTAS A BOTONES
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user = query.from_user
    print(f"[LOG] {user.full_name} (@{user.username}) seleccionó: {data}")

    if data == "info_premium":
        await query.edit_message_text(
            text="El costo de entrada al grupo es de 499 pesos mexicanos (25 USD) mensuales.\n"
                 "👉 [Haz clic aquí para pagar](https://app.buclecompany.com/v2/preview/cpmzsZAJYGx3tkxtirBf?notrack=true)",
            parse_mode="Markdown"
        )
    elif data == "faq":
        keyboard = [
            [InlineKeyboardButton("1. Porcentaje de ganancias", callback_data="faq_1")],
            [InlineKeyboardButton("2. Plataforma de apuestas", callback_data="faq_2")],
            [InlineKeyboardButton("3. Duda de pick", callback_data="faq_3")],
            [InlineKeyboardButton("4. Otra pregunta", callback_data="faq_4")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Preguntas frecuentes:\nSelecciona una opción:",
            reply_markup=reply_markup
        )
    elif data == "faq_1":
        await query.edit_message_text(text="El grupo tiene un promedio de 85-90% de aciertos mensuales.")
    elif data == "faq_2":
        await query.edit_message_text(text="Usamos Bet365, 1XBet y Codere.")
    elif data == "faq_3":
        await query.edit_message_text(text="Escribe tu duda sobre un pick y un admin te contestará.")
    elif data == "faq_4":
        await query.edit_message_text(text="Escribe tu pregunta, será atendida directamente.")

# FALLBACK
async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

# FUNCIÓN DE EJECUCIÓN PRINCIPAL
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))

    print("✅ Bot corriendo correctamente en Railway...")
    app.run_polling()

if __name__ == "__main__":
    main()
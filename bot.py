import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

# Cargar las variables de entorno
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = 6130272246  # Reemplazar por el ID real del administrador

# Menú principal
main_menu = ReplyKeyboardMarkup(
    [["1. Información sobre el grupo premium"], ["2. Preguntas frecuentes"], ["3. Otra duda"]],
    resize_keyboard=True
)

# Submenú de preguntas frecuentes
faq_menu = ReplyKeyboardMarkup(
    [["1. Porcentaje de ganancias"], ["2. Plataforma de apuestas"], ["3. Duda de pick"], ["4. Otra pregunta"]],
    resize_keyboard=True
)

# Estado de usuarios esperando pregunta libre
dynamic_state = {}

# Mensaje inicial o cualquier palabra activa el menú
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    dynamic_state.pop(user_id, None)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="¡Hola! 👋 ¿Cómo puedo ayudarte hoy?",
                                   reply_markup=main_menu)

# Manejo de mensajes
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id in dynamic_state:
        # El usuario está respondiendo una duda libre
        motivo = dynamic_state.pop(user_id)
        mensaje = f"📩 Nueva duda desde el bot:\nID: {user_id}\nMotivo: {motivo}\nMensaje: {text}"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=mensaje)
        await update.message.reply_text("Gracias, un administrador te responderá en breve.")
        return

    if text == "1. Información sobre el grupo premium":
        await update.message.reply_text("El costo de entrada al grupo es de 499 MXN (25 USD) mensuales.\n\n👉 Paga aquí: https://tu-link-de-pago.com")
    elif text == "2. Preguntas frecuentes":
        await update.message.reply_text("Preguntas frecuentes:\nSelecciona una opción:", reply_markup=faq_menu)
    elif text == "3. Otra duda":
        dynamic_state[user_id] = "Otra duda"
        await update.message.reply_text("Por favor, escribe tu pregunta y te responderemos manualmente en breve.")
    elif text == "1. Porcentaje de ganancias":
        await update.message.reply_text("El porcentaje de ganancias mensual es del 85% aproximado.")
    elif text == "2. Plataforma de apuestas":
        await update.message.reply_text("Usamos mayormente Bet365 y Caliente.mx para nuestros picks.")
    elif text == "3. Duda de pick":
        dynamic_state[user_id] = "Duda sobre pick"
        await update.message.reply_text("Escribe tu duda sobre un pick. Un administrador te responderá personalmente.")
    elif text == "4. Otra pregunta":
        dynamic_state[user_id] = "Otra pregunta en FAQs"
        await update.message.reply_text("Por favor, escribe tu pregunta.")
    else:
        await update.message.reply_text("No entendí esa opción. Por favor elige una del menú.", reply_markup=main_menu)

# Inicialización del bot
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot corriendo correctamente en Railway...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio

    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError:
        # fallback si el loop ya está corriendo
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())

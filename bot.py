import os
from dotenv import load_dotenv
from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Opciones del menú principal
MAIN_MENU = [
    "1. Información sobre el grupo premium",
    "2. Preguntas frecuentes"
]

# Opciones del submenú de FAQ
FAQ_OPTIONS = [
    "1. Porcentaje de ganancias",
    "2. Plataforma de apuestas",
    "3. Otra duda",
    "4. Volver al menú principal"
]

# Mensaje inicial al escribir /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton(opt)] for opt in MAIN_MENU]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("¡Hola! 👋 ¿Cómo puedo ayudarte hoy?", reply_markup=reply_markup)
    context.user_data["submenu"] = None  # Reinicia estado

# Manejador de mensajes escritos
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "1. Información sobre el grupo premium":
        await update.message.reply_text("El costo de entrada al grupo es de 499 MXN (25 USD) mensuales.\n👉 Paga aquí")

    elif text == "2. Preguntas frecuentes":
        if context.user_data.get("submenu") != "faq":
            keyboard = [[KeyboardButton(opt)] for opt in FAQ_OPTIONS]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("Preguntas frecuentes:\nSelecciona una opción:", reply_markup=reply_markup)
            context.user_data["submenu"] = "faq"

    elif text == "1. Porcentaje de ganancias":
        await update.message.reply_text("Actualmente manejamos un porcentaje mensual estimado entre 10% y 35%.")

    elif text == "2. Plataforma de apuestas":
        await update.message.reply_text("La plataforma principal que usamos es Bet365, aunque también damos picks para Codere o Caliente.")

    elif text == "3. Otra duda":
        await update.message.reply_text("Escribe tu duda sobre un pick. Un administrador te responderá personalmente.")

    elif text == "4. Volver al menú principal":
        keyboard = [[KeyboardButton(opt)] for opt in MAIN_MENU]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Menú principal:", reply_markup=reply_markup)
        context.user_data["submenu"] = None

    else:
        await update.message.reply_text("No entendí esa opción. Por favor elige una del menú.")

# Función principal
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot corriendo correctamente en Railway...")
    await app.run_polling()

# Ejecutar
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
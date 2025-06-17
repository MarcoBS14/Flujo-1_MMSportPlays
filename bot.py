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

# Cargar token desde variables de entorno
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Menús
MAIN_MENU = [
    "1. Información sobre el grupo premium",
    "2. Preguntas frecuentes"
]
FAQ_OPTIONS = [
    "1. Porcentaje de ganancias",
    "2. Plataforma de apuestas",
    "3. Otra duda",
    "4. Volver al menú principal"
]

def make_keyboard(options):
    return ReplyKeyboardMarkup([[KeyboardButton(opt)] for opt in options], resize_keyboard=True)

# /start o cualquier texto
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["submenu"] = None
    await update.message.reply_text(
        "¡Hola! 👋 ¿Cómo puedo ayudarte hoy?",
        reply_markup=make_keyboard(MAIN_MENU)
    )

# Mensajes del usuario
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip()
    submenu = context.user_data.get("submenu", None)

    # Si no hay submenú y mensaje no es válido, mostrar siempre el menú principal
    if submenu is None:
        if msg == MAIN_MENU[0]:
            await update.message.reply_text("El costo de entrada al grupo es de 499 MXN (25 USD) mensuales.\n👉 Paga aquí")
        elif msg == MAIN_MENU[1]:
            context.user_data["submenu"] = "faq"
            await update.message.reply_text("Preguntas frecuentes:\nSelecciona una opción:", reply_markup=make_keyboard(FAQ_OPTIONS))
        else:
            await start(update, context)  # Redirige al menú principal
        return

    # Submenú de FAQ
    if submenu == "faq":
        if msg == FAQ_OPTIONS[0]:
            await update.message.reply_text("Actualmente manejamos un porcentaje mensual estimado entre 10% y 35%.")
        elif msg == FAQ_OPTIONS[1]:
            await update.message.reply_text("La plataforma principal que usamos es Bet365, aunque también damos picks para Codere o Caliente.")
        elif msg == FAQ_OPTIONS[2]:
            await update.message.reply_text("Escribe tu duda sobre un pick. Un administrador te responderá personalmente.")
        elif msg == FAQ_OPTIONS[3]:
            context.user_data["submenu"] = None
            await start(update, context)
        else:
            await update.message.reply_text("No entendí esa opción. Por favor elige una del menú.")

# Main
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot corriendo correctamente...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
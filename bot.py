import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

user_context = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    user_context[user_id] = "main_menu"
    keyboard = [["1. Información sobre el grupo premium"], ["2. Preguntas frecuentes"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("¡Hola! 👋 ¿Cómo puedo ayudarte hoy?", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    text = update.message.text.strip().lower()
    state = user_context.get(user_id, "main_menu")

    if state == "main_menu":
        if text.startswith("1"):
            await update.message.reply_text(
                "El costo de entrada al grupo es de 499 MXN (25 USD) mensuales.\n\n👉 [Paga aquí](https://app.buclecompany.com/v2/preview/cpmzsZAJYGx3tkxtirBf?notrack=true)",
                parse_mode="Markdown"
            )
        elif text.startswith("2"):
            user_context[user_id] = "faq_menu"
            keyboard = [
                ["1. Porcentaje de ganancias"],
                ["2. Plataforma de apuestas"],
                ["3. Duda de pick"],
                ["4. Otra pregunta"],
                ["⬅️ Volver"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("Preguntas frecuentes:\nSelecciona una opción:", reply_markup=reply_markup)
        else:
            await update.message.reply_text("Por favor, selecciona una opción válida.")
    elif state == "faq_menu":
        if text.startswith("1"):
            await update.message.reply_text("El grupo ha mantenido un promedio de 85-90% de aciertos mensuales.\nLas estadísticas se comparten semanalmente.")
        elif text.startswith("2"):
            await update.message.reply_text("Usamos plataformas como Bet365, 1XBet y Codere.")
        elif text.startswith("3"):
            await update.message.reply_text("Por favor, escribe tu duda sobre un pick. Un administrador te responderá personalmente.")
        elif text.startswith("4"):
            await update.message.reply_text("Por favor, escribe tu pregunta. Será atendida directamente por un miembro del equipo.")
        elif "volver" in text:
            return await start(update, context)
        else:
            await update.message.reply_text("Selecciona una opción válida del submenú.")

# Construcción de la app
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    import asyncio
    async def main():
        print("✅ Bot corriendo correctamente en Railway...")
        await app.run_polling()
    asyncio.run(main())
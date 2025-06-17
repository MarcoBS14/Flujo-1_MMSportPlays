import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# MENU PRINCIPAL
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["1. Información sobre el grupo premium", "2. Preguntas frecuentes"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("¡Hola! ¿Cómo puedo ayudarte hoy?", reply_markup=reply_markup)

# RESPUESTAS SEGÚN TEXTO
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "información" in text or "1." in text:
        await update.message.reply_text(
            "El costo de entrada al grupo es de 499 MXN (25 USD) mensuales.\n"
            "👉 [Paga aquí](https://app.buclecompany.com/v2/preview/cpmzsZAJYGx3tkxtirBf?notrack=true)",
            parse_mode="Markdown"
        )

    elif "preguntas" in text or "2." in text:
        faq_keyboard = [
            ["1. Porcentaje de ganancias", "2. Plataforma de apuestas"],
            ["3. Duda de pick", "4. Otra pregunta"]
        ]
        reply_markup = ReplyKeyboardMarkup(faq_keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Preguntas frecuentes:\nSelecciona una opción:", reply_markup=reply_markup)

    elif "porcentaje" in text or "1." in text:
        await update.message.reply_text("Mantenemos un promedio de 85-90% de aciertos mensuales.")

    elif "plataforma" in text or "2." in text:
        await update.message.reply_text("Usamos plataformas como Bet365, 1XBet y Codere.")

    elif "duda" in text or "3." in text:
        await update.message.reply_text("Escribe tu duda sobre un pick. Un administrador te responderá personalmente.")

    elif "otra" in text or "4." in text:
        await update.message.reply_text("Por favor, escribe tu pregunta. Será atendida directamente.")

    else:
        await start(update, context)  # volver a mostrar el menú

# INICIO
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot corriendo con teclado normal...")
    app.run_polling()

if __name__ == "__main__":
    main()
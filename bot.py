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

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# MENSAJE DE MENÚ INICIAL
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["1. Información sobre el grupo premium"], ["2. Preguntas frecuentes"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("¡Hola! 👋 ¿Cómo puedo ayudarte hoy?", reply_markup=reply_markup)

# RESPUESTA A OPCIONES DEL MENÚ
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == "1" or text.startswith("1."):
        await update.message.reply_text("El costo de entrada al grupo es de 499 MXN (25 USD) mensuales.\n👉 Paga aquí")
    elif text == "2" or text.startswith("2."):
        keyboard = [
            ["1. Porcentaje de ganancias"],
            ["2. Plataforma de apuestas"],
            ["3. Duda de pick"],
            ["4. Otra pregunta"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Preguntas frecuentes:\nSelecciona una opción:", reply_markup=reply_markup)

    elif text.startswith("1. Porcentaje") or text == "1":
        await update.message.reply_text("El porcentaje de ganancias varía, pero suele estar entre 60% y 80% mensual.")
    elif text.startswith("2. Plataforma") or text == "2":
        await update.message.reply_text("La plataforma recomendada para las apuestas es Bet365.")
    elif text.startswith("3. Duda") or text == "3":
        await update.message.reply_text("Escribe tu duda sobre un pick. Un administrador te responderá personalmente.")
    elif text.startswith("4. Otra") or text == "4":
        await update.message.reply_text("Por favor, escribe tu pregunta y te responderemos lo antes posible.")
    else:
        # Si no reconoce el texto, vuelve a mostrar el menú
        await start(update, context)

# CONFIGURACIÓN PRINCIPAL
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot corriendo correctamente en Railway...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
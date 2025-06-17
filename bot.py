import logging
import os
import asyncio
import nest_asyncio
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Carga variables de entorno
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Configura logging
logging.basicConfig(level=logging.INFO)

# Menú principal
menu_principal = [["1. Información del grupo premium", "2. Preguntas frecuentes"]]
submenu_preguntas = [["1. % de ganancias", "2. Plataforma"],
                     ["3. Duda sobre pick", "4. Otra pregunta"]]

# Función para mostrar menú principal
async def mostrar_menu_principal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Selecciona una opción:",
        reply_markup=ReplyKeyboardMarkup(menu_principal, one_time_keyboard=True, resize_keyboard=True)
    )

# Función para mostrar submenu
async def mostrar_submenu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Preguntas frecuentes:",
        reply_markup=ReplyKeyboardMarkup(submenu_preguntas, one_time_keyboard=True, resize_keyboard=True)
    )

# Función para manejar cualquier texto
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "1" in text and "premium" in text:
        await update.message.reply_text("El grupo premium ofrece picks diarios con análisis detallado...")

    elif "2" in text and "frecuentes" in text:
        await mostrar_submenu(update, context)

    elif "1" in text and "ganancias" in text:
        await update.message.reply_text("El porcentaje de ganancias varía, pero actualmente es del 78% mensual.")

    elif "2" in text and "plataforma" in text:
        await update.message.reply_text("Usamos Bet365 por su confiabilidad y facilidad de uso.")

    elif "3" in text or "duda" in text:
        await update.message.reply_text("Escribe tu duda sobre el pick y nuestro equipo te responderá.")

    elif "4" in text or "otra" in text:
        await update.message.reply_text("Por favor, escribe tu pregunta y un miembro del equipo la atenderá.")

    else:
        await mostrar_menu_principal(update, context)

# Función principal
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", mostrar_menu_principal))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("✅ Bot corriendo correctamente en Railway...")
    await app.run_polling()

# Evitar errores con event loop en Railway
if __name__ == "__main__":
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
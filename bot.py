import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    ConversationHandler,
)
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_CHAT_ID = 6130272246  # Tu chat_id personal

# Configuración del log
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Estados para ConversationHandler
WAITING_FOR_QUESTION = range(1)

# Menú principal
main_menu = ReplyKeyboardMarkup(
    [
        [KeyboardButton("1. Información del grupo premium")],
        [KeyboardButton("2. Preguntas frecuentes")],
        [KeyboardButton("3. Tengo una duda sobre un pick")]
    ],
    resize_keyboard=True
)

# Submenú (puedes expandir esto si deseas)
faq_menu = ReplyKeyboardMarkup(
    [
        [KeyboardButton("1. Porcentaje de ganancias")],
        [KeyboardButton("2. Plataforma de apuestas")],
        [KeyboardButton("3. Otra pregunta")]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Bienvenido! Selecciona una opción:", reply_markup=main_menu)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text.startswith("/start") or text.lower() in ["hola", "menu", "inicio"]:
        await update.message.reply_text("¡Bienvenido! Selecciona una opción:", reply_markup=main_menu)
        return

    if text.startswith("1. Información del grupo premium"):
        await update.message.reply_text("El grupo premium incluye picks exclusivos, seguimiento personalizado y más.")
    elif text.startswith("2. Preguntas frecuentes"):
        await update.message.reply_text("Selecciona una pregunta frecuente:", reply_markup=faq_menu)
    elif text.startswith("3. Tengo una duda sobre un pick"):
        await update.message.reply_text("Por favor escribe tu duda y la enviaré al administrador.")
        return WAITING_FOR_QUESTION
    elif text.startswith("1. Porcentaje de ganancias"):
        await update.message.reply_text("Nuestro porcentaje de ganancias promedio es del 85% mensual.")
    elif text.startswith("2. Plataforma de apuestas"):
        await update.message.reply_text("Recomendamos utilizar Bet365, Codere o Caliente MX.")
    elif text.startswith("3. Otra pregunta"):
        await update.message.reply_text("Escribe tu pregunta y la enviaré al administrador.")
        return WAITING_FOR_QUESTION
    else:
        await update.message.reply_text("No entendí tu mensaje. Por favor elige una opción del menú.")

async def forward_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    question = update.message.text

    mensaje = f"📩 Nueva pregunta de {user.full_name} (@{user.username}):\n\n{question}"
    await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=mensaje)

    await update.message.reply_text("Gracias por tu pregunta. El administrador te responderá pronto.", reply_markup=main_menu)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operación cancelada.", reply_markup=main_menu)
    return ConversationHandler.END

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^3. Tengo una duda sobre un pick$"), handle_message),
            MessageHandler(filters.Regex("^3. Otra pregunta$"), handle_message)
        ],
        states={
            WAITING_FOR_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, forward_question)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
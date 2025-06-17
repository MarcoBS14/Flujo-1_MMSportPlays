import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

# Carga del token desde las variables de entorno (.env o Railway)
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# MENSAJE INICIAL
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("1. Información sobre el grupo premium", callback_data="info_premium")],
        [InlineKeyboardButton("2. Preguntas frecuentes", callback_data="faq")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("¡Hola! 👋 ¿Cómo puedo ayudarte hoy?", reply_markup=reply_markup)

# MANEJO DE BOTONES
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    match query.data:
        case "info_premium":
            await query.edit_message_text(
                text="El costo de entrada al grupo es de 499 pesos mexicanos (25 USD) mensuales.\n"
                     "Al hacer el pago y compartir el comprobante, se te agrega al grupo.\n"
                     "👉 [Haz clic aquí para pagar](https://app.buclecompany.com/v2/preview/cpmzsZAJYGx3tkxtirBf?notrack=true)",
                parse_mode="Markdown"
            )
        case "faq":
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
        case "faq_1":
            await query.edit_message_text(
                text="El grupo ha mantenido un promedio de 85-90% de aciertos mensuales.\nLas estadísticas se comparten semanalmente."
            )
        case "faq_2":
            await query.edit_message_text(
                text="Usamos plataformas como Bet365, 1XBet y Codere."
            )
        case "faq_3":
            await query.edit_message_text(
                text="Por favor, escribe tu duda sobre un pick. Un administrador te responderá personalmente."
            )
        case "faq_4":
            await query.edit_message_text(
                text="Por favor, escribe tu pregunta. Será atendida directamente por un miembro del equipo."
            )
        case _:
            await query.edit_message_text(text="❌ Opción no reconocida.")

# MENSAJES DE TEXTO NO COMANDOS
async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

# EJECUCIÓN PRINCIPAL
if __name__ == "__main__":
    import asyncio

    async def main():
        app = ApplicationBuilder().token(TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(handle_button))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))

        print("✅ Bot corriendo correctamente en Railway...")
        await app.run_polling()

    asyncio.run(main())
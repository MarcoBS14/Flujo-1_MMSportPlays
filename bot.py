import os
import unicodedata
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = 6130272246  # Reemplaza con tu ID real

# Menú principal (solo opciones 1 y 2)
main_menu = ReplyKeyboardMarkup(
    [["1. Información sobre el grupo premium"], ["2. Preguntas frecuentes"]],
    resize_keyboard=True
)

# Submenú de FAQs (opciones 1 a 4, incluyendo dudas)
faq_menu = ReplyKeyboardMarkup(
    [["1. Porcentaje de ganancias"], ["2. Plataforma de apuestas"], ["3. Duda de pick"], ["4. Otra pregunta"]],
    resize_keyboard=True
)

# Diccionario de estados por usuario
dynamic_state = {}

# Normalización de texto (quitar tildes y pasar a minúsculas)
def normalizar(texto):
    texto = texto.lower()
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

# /start o mensaje libre → muestra menú principal
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.effective_user.id)
    dynamic_state.pop(user_id, None)  # Limpiar estado previo
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="¡Hola! 👋 ¿Cómo puedo ayudarte hoy?",
        reply_markup=main_menu
    )

# Manejo general de mensajes
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.effective_user.id)
    text_raw = update.message.text.strip()
    text = normalizar(text_raw)

    # Si el usuario está respondiendo una duda
    if user_id in dynamic_state:
        motivo = dynamic_state.pop(user_id)
        mensaje = f"📩 Nueva duda desde el bot:\nID: {user_id}\nMotivo: {motivo}\nMensaje: {text_raw}"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=mensaje)
        await update.message.reply_text("Gracias, un administrador te responderá en breve.")
        return

    # Menú principal
    if text_raw == "1. Información sobre el grupo premium":
        await update.message.reply_text(
            "El costo de entrada al grupo es de 499 MXN (25 USD) mensuales.\n\n👉 Paga aquí: https://tu-link-de-pago.com"
        )
        return

    elif text_raw == "2. Preguntas frecuentes":
        await update.message.reply_text(
            "Preguntas frecuentes:\nSelecciona una opción:",
            reply_markup=faq_menu
        )
        return

    # Submenú de FAQs
    elif text_raw == "1. Porcentaje de ganancias":
        await update.message.reply_text("El porcentaje de ganancias mensual es del 85% aproximado.")
        return

    elif text_raw == "2. Plataforma de apuestas":
        await update.message.reply_text("Usamos mayormente Bet365 y Caliente.mx para nuestros picks.")
        return

    elif text_raw == "3. Duda de pick":
        dynamic_state[user_id] = "Duda sobre pick"
        await update.message.reply_text("Escribe tu duda sobre un pick. Un administrador te responderá personalmente.")
        return

    elif text_raw == "4. Otra pregunta":
        dynamic_state[user_id] = "Otra pregunta en FAQs"
        await update.message.reply_text("Por favor, escribe tu pregunta.")
        return

    # Fallback para cualquier otro texto: muestra menú principal
    await update.message.reply_text(
        "¡Hola! 👋 ¿Cómo puedo ayudarte hoy?",
        reply_markup=main_menu
    )

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
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
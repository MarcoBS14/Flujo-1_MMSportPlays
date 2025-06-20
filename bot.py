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
ADMIN_CHAT_ID = 6130272246

# Teclado del menú principal
main_menu_keyboard = [
    ["1. Información sobre el grupo premium"],
    ["2. Preguntas frecuentes"]
]
main_menu = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

# Teclado del submenú FAQ
faq_menu_keyboard = [
    ["1. Porcentaje de ganancias"],
    ["2. Plataforma de apuestas"],
    ["3. Duda de pick"],
    ["4. Otra pregunta"]
]
faq_menu = ReplyKeyboardMarkup(faq_menu_keyboard, resize_keyboard=True)

# Diccionario para el estado del usuario
dynamic_state = {}

# Normalizador de texto
def normalizar(texto):
    texto = texto.lower()
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.effective_user.id)
    dynamic_state.pop(user_id, None)

    await update.message.reply_text(
        "¡Hola! 👋 ¿Cómo puedo ayudarte hoy?",
        reply_markup=main_menu
    )

# Manejo de texto
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.effective_user.id)
    text_raw = update.message.text.strip()
    text = normalizar(text_raw)

    # Si el usuario está en modo de respuesta
    if user_id in dynamic_state:
        motivo = dynamic_state.pop(user_id)
        mensaje = f"📩 Nueva duda:\nID: {user_id}\nMotivo: {motivo}\nMensaje: {text_raw}"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=mensaje)
        await update.message.reply_text("Gracias. Un administrador te responderá pronto.")
        return

    # Menú principal
    if text_raw == "1. Información sobre el grupo premium":
        await update.message.reply_text(
            "El costo de entrada al grupo es de 499 MXN (25 USD) mensuales.\n\n👉 Paga aquí: https://app.buclecompany.com/v2/preview/cpmzsZAJYGx3tkxtirBf?notrack=true"
        )
        return

    elif text_raw == "2. Preguntas frecuentes":
        await update.message.reply_text(
            "Selecciona una pregunta frecuente:",
            reply_markup=faq_menu
        )
        return

    # Submenú FAQ
    elif text_raw == "1. Porcentaje de ganancias":
        await update.message.reply_text("El porcentaje de ganancias mensual es de aproximadamente 85%.")
        return

    elif text_raw == "2. Plataforma de apuestas":
        await update.message.reply_text("Usamos principalmente Bet365 y Caliente.mx para nuestros picks.")
        return

    elif text_raw == "3. Duda de pick":
        dynamic_state[user_id] = "Duda sobre pick"
        await update.message.reply_text("Por favor escribe tu duda. Un administrador la recibirá.")
        return

    elif text_raw == "4. Otra pregunta":
        dynamic_state[user_id] = "Otra pregunta"
        await update.message.reply_text("Escribe tu pregunta y te responderemos en breve.")
        return

    # Fallback
    await update.message.reply_text("No entendí eso. Por favor selecciona una opción del menú.", reply_markup=main_menu)

# Inicialización de la app
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("✅ Bot corriendo correctamente...")
    app.run_polling()
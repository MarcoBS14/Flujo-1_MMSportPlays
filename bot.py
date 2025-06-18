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
ADMIN_CHAT_ID = 6130272246  # Reemplaza con el ID real del administrador

# Menú principal (solo opciones 1 y 2)
main_menu = ReplyKeyboardMarkup(
    [["1. Información sobre el grupo premium"], ["2. Preguntas frecuentes"]],
    resize_keyboard=True
)

# Submenú (FAQs con 4 opciones)
faq_menu = ReplyKeyboardMarkup(
    [["1. Porcentaje de ganancias"], ["2. Plataforma de apuestas"], ["3. Duda de pick"], ["4. Otra pregunta"]],
    resize_keyboard=True
)

# Diccionario de estados activos
dynamic_state = {}

# Función para normalizar texto
def normalizar(texto):
    texto = texto.lower()
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

# Comando /start o mensajes de activación
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.effective_user.id)
    dynamic_state.pop(user_id, None)
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

    # Si está en modo de espera para escribir su duda
    if user_id in dynamic_state:
        motivo = dynamic_state.pop(user_id)
        mensaje = f"📩 Nueva duda desde el bot:\nID: {user_id}\nMotivo: {motivo}\nMensaje: {text_raw}"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=mensaje)
        await update.message.reply_text("Gracias, un administrador te responderá en breve.")
        return

    # Menú principal
    if text_raw == "1. Información sobre el grupo premium":
        await update.message.reply_text(
            "El costo de entrada al grupo es de 499 MXN (25 USD) mensuales.\n\n👉 Paga aquí: https://app.buclecompany.com/v2/preview/cpmzsZAJYGx3tkxtirBf?notrack=true "
        )
        return

    elif text_raw == "2. Preguntas frecuentes":
        await update.message.reply_text(
            "Preguntas frecuentes:\nSelecciona una opción:",
            reply_markup=faq_menu
        )
        return

    # Submenú
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

    # Fallback: cualquier otro mensaje → menú principal
    await update.message.reply_text(
        "¡Hola! 👋 ¿Cómo puedo ayudarte hoy?",
        reply_markup=main_menu
    )

# Inicialización directa sin manejo manual del loop (recomendado para Railway)
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot corriendo correctamente en Railway...")
    app.run_polling()
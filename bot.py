import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
)

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = 6130272246

# Diccionario de estados activos
estado_usuario = {}

# Menús con botones inline
main_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("📌 Información sobre el grupo premium", callback_data="info")],
    [InlineKeyboardButton("📋 Preguntas frecuentes", callback_data="faq")]
])

faq_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("📈 Porcentaje de ganancias", callback_data="faq_1")],
    [InlineKeyboardButton("📲 Plataforma de apuestas", callback_data="faq_2")],
    [InlineKeyboardButton("❓ Duda de pick", callback_data="faq_3")],
    [InlineKeyboardButton("🗣️ Otra pregunta", callback_data="faq_4")]
])

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ¡Hola! ¿Cómo puedo ayudarte hoy?",
        reply_markup=main_menu
    )

# Interacción con botones
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == "info":
        await query.edit_message_text(
            "💰 El costo del grupo premium es de 499 MXN mensuales.\n\n👉 Paga aquí: https://app.buclecompany.com/v2/preview/cpmzsZAJYGx3tkxtirBf?notrack=true"
        )

    elif data == "faq":
        await query.edit_message_text("Selecciona una pregunta frecuente:", reply_markup=faq_menu)

    elif data == "faq_1":
        await query.edit_message_text("📈 El porcentaje de ganancias mensual es del 85% aproximado.")

    elif data == "faq_2":
        await query.edit_message_text("📲 Usamos Bet365 y Caliente.mx para nuestros picks.")

    elif data == "faq_3":
        estado_usuario[user_id] = "pick"
        await query.edit_message_text("✏️ Escribe tu duda sobre un pick y se la enviaremos al administrador.")

    elif data == "faq_4":
        estado_usuario[user_id] = "otra"
        await query.edit_message_text("✏️ Por favor, escribe tu pregunta y se la enviaremos al administrador.")

# Respuesta textual del usuario
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id in estado_usuario:
        motivo = estado_usuario.pop(user_id)
        mensaje = f"📩 Nueva duda desde el bot:\nID: {user_id}\nMotivo: {motivo}\nMensaje: {text}"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=mensaje)
        await update.message.reply_text("✅ Gracias. Un administrador te responderá en breve.")
    else:
        await update.message.reply_text("Por favor, selecciona una opción del menú:", reply_markup=main_menu)

# Lanzar aplicación
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("✅ Bot de leads desplegado correctamente.")
    app.run_polling()
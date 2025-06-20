import os
from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = 6130272246

# Estado de usuarios que escriben preguntas
estado_usuario = {}

# Menú principal con botones inline
main_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("📈 Información sobre el grupo premium", callback_data="info")],
    [InlineKeyboardButton("❓ Preguntas frecuentes", callback_data="faq")]
])

# Submenú de preguntas frecuentes
faq_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("📊 Porcentaje de ganancias", callback_data="faq_1")],
    [InlineKeyboardButton("📱 Plataforma de apuestas", callback_data="faq_2")],
    [InlineKeyboardButton("🤔 Duda de pick", callback_data="faq_3")],
    [InlineKeyboardButton("💬 Otra pregunta", callback_data="faq_4")]
])

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ¡Hola! ¿Cómo puedo ayudarte hoy?",
        reply_markup=main_menu
    )

# Manejo de botones
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "info":
        await query.edit_message_text(
            "💡 El grupo premium incluye acceso diario a picks deportivos exclusivos.\n\n"
            "📌 Precio: 499 MXN al mes\n"
            "👉 Paga aquí: https://app.buclecompany.com/v2/preview/cpmzsZAJYGx3tkxtirBf?notrack=true"
        )
    elif data == "faq":
        await query.edit_message_text(
            "📋 Preguntas frecuentes:",
            reply_markup=faq_menu
        )
    elif data == "faq_1":
        await query.edit_message_text("📊 Nuestro porcentaje de ganancias mensual es del 85% aproximado.")
    elif data == "faq_2":
        await query.edit_message_text("📱 Usamos Bet365 y Caliente.mx para nuestros picks.")
    elif data == "faq_3":
        estado_usuario[user_id] = "Duda sobre pick"
        await query.edit_message_text("✏️ Escribe tu duda sobre un pick:")
    elif data == "faq_4":
        estado_usuario[user_id] = "Otra pregunta"
        await query.edit_message_text("✏️ Por favor, escribe tu pregunta y un asesor te responderá.")
    else:
        await query.edit_message_text("❌ Opción no válida.")

# Manejo de mensajes de texto (dudas)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    mensaje = update.message.text.strip()

    if user_id in estado_usuario:
        motivo = estado_usuario.pop(user_id)
        texto = f"📩 Nueva pregunta:\n👤 ID: {user_id}\n📝 Motivo: {motivo}\n💬 Mensaje: {mensaje}"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=texto)
        await update.message.reply_text("✅ Gracias, un administrador te responderá en breve.")
    else:
        await update.message.reply_text("Selecciona una opción usando el menú 👇", reply_markup=main_menu)

# Inicialización del bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot de leads en ejecución...")
    app.run_polling()
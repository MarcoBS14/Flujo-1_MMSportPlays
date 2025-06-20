import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Cargar variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = 6130272246

# Menú principal (Inline buttons)
main_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("📌 Información sobre el grupo premium", callback_data="info")],
    [InlineKeyboardButton("❓ Preguntas frecuentes", callback_data="faq")]
])

# Submenú FAQ
faq_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ Porcentaje de ganancias", callback_data="faq_1")],
    [InlineKeyboardButton("2️⃣ Plataforma de apuestas", callback_data="faq_2")],
    [InlineKeyboardButton("3️⃣ Duda de pick", callback_data="faq_3")],
    [InlineKeyboardButton("4️⃣ Otra pregunta", callback_data="faq_4")]
])

# Estado para capturar dudas escritas
estado_usuario = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! 👋 ¿Cómo puedo ayudarte hoy?",
        reply_markup=main_menu
    )

# Interacción con los botones
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    # Opciones del menú principal
    if data == "info":
        await query.edit_message_text(
            "El costo de entrada al grupo es de 499 MXN (25 USD) mensuales.\n\n👉 Paga aquí: https://app.buclecompany.com/v2/preview/cpmzsZAJYGx3tkxtirBf?notrack=true"
        )
    elif data == "faq":
        await query.edit_message_text("Selecciona una pregunta frecuente:", reply_markup=faq_menu)

    # Submenú FAQ
    elif data == "faq_1":
        await query.edit_message_text("📈 El porcentaje de ganancias mensual es de aproximadamente 85%.")
    elif data == "faq_2":
        await query.edit_message_text("🎯 Usamos principalmente Bet365 y Caliente.mx para nuestros picks.")
    elif data == "faq_3":
        estado_usuario[user_id] = "duda_pick"
        await query.edit_message_text("✏️ Por favor, escribe tu duda sobre el pick.")
    elif data == "faq_4":
        estado_usuario[user_id] = "otra_pregunta"
        await query.edit_message_text("✏️ Por favor, escribe tu pregunta.")

# Capturar dudas escritas
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    mensaje = update.message.text.strip()

    if user_id in estado_usuario:
        motivo = estado_usuario.pop(user_id)
        texto = f"📩 Nueva duda:\n🧑 ID: {user_id}\n📝 Motivo: {motivo}\n💬 Mensaje: {mensaje}"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=texto)
        await update.message.reply_text("Gracias. Un administrador te responderá pronto.")
    else:
        await update.message.reply_text("Por favor selecciona una opción del menú usando los botones.")

# Inicialización
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(CommandHandler("menu", start))  # Por si quiere regresar
    app.add_handler(CommandHandler("inicio", start))
    app.add_handler(CommandHandler("ayuda", start))
    app.add_handler(CommandHandler("volver", start))
    app.add_handler(CommandHandler("home", start))
    app.add_handler(CommandHandler("main", start))
    app.add_handler(CommandHandler("regresar", start))
    app.add_handler(CommandHandler("cancelar", start))

    # Si escribe una duda después de FAQ
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

    print("✅ Bot corriendo correctamente...")
    app.run_polling()
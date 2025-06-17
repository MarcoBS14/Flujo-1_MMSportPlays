import asyncio
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder, CallbackQueryHandler, CommandHandler,
    MessageHandler, ContextTypes, filters
)
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_CHAT_ID = os.getenv("OWNER_CHAT_ID")  # Pega aquí el número cuando lo tengas

# --- MENÚ PRINCIPAL ---
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1. Info Grupo Premium", callback_data='1')],
        [InlineKeyboardButton("2. Preguntas frecuentes", callback_data='2')]
    ])

# --- SUBMENÚ FAQ ---
def faq_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1. Porcentaje de ganancias", callback_data='faq_1')],
        [InlineKeyboardButton("2. Plataforma de apuestas", callback_data='faq_2')],
        [InlineKeyboardButton("3. Duda de pick", callback_data='faq_3')],
        [InlineKeyboardButton("4. Otra pregunta", callback_data='faq_4')]
    ])

# --- /start o cualquier texto muestra el menú ---
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Bienvenido! Elige una opción:", reply_markup=main_menu_keyboard())

# --- Captura el chat ID del dueño y lo responde (temporal) ---
async def get_owner_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"🆔 Tu chat ID es: `{chat_id}`", parse_mode="Markdown")

# --- Manejador de botones ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    # Menú principal
    if data == '1':
        await query.message.reply_text("🔐 El grupo premium ofrece picks diarios y soporte personalizado.")
    elif data == '2':
        await query.message.reply_text("Preguntas frecuentes:", reply_markup=faq_menu_keyboard())

    # Submenú FAQ
    elif data == 'faq_1':
        await query.message.reply_text("📈 El porcentaje de ganancias es del 80% mensual aproximadamente.")
    elif data == 'faq_2':
        await query.message.reply_text("🏟️ Usamos plataformas legales como Bet365 y Caliente.mx.")
    elif data == 'faq_3':
        await query.message.reply_text("✍️ Por favor, escribe tu duda sobre el pick aquí.")
        context.user_data['waiting_question'] = 'duda_pick'
    elif data == 'faq_4':
        await query.message.reply_text("✍️ Por favor, escribe tu pregunta aquí.")
        context.user_data['waiting_question'] = 'otra_pregunta'

# --- Reenvío de dudas al dueño ---
async def forward_doubt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting_question'):
        message = update.message.text
        user = update.effective_user
        text = f"📩 Nueva pregunta de {user.first_name} (@{user.username or 'sin usuario'}):\n\n{message}"

        if OWNER_CHAT_ID:
            await context.bot.send_message(chat_id=int(OWNER_CHAT_ID), text=text)

        await update.message.reply_text("✅ Gracias por tu mensaje. Pronto te responderemos.")
        context.user_data['waiting_question'] = None
    else:
        await handle_text(update, context)  # Muestra el menú si no estaba esperando pregunta

# --- MAIN ---
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", handle_text))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Detectar cualquier texto
    app.add_handler(MessageHandler(filters.TEXT & filters.User(username="tu_usuario_telegram"), get_owner_chat_id))  # Solo para que obtengas tu chat_id
    app.add_handler(MessageHandler(filters.TEXT, forward_doubt))

    print("✅ Bot corriendo correctamente en Railway...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
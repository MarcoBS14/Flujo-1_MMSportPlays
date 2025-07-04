import os
from dotenv import load_dotenv
import unicodedata
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

# Menú principal
main_menu = ReplyKeyboardMarkup(
    [["1. Información sobre el grupo premium"], ["2. Preguntas frecuentes"]],
    resize_keyboard=True
)

# Submenú de preguntas frecuentes
faq_menu = ReplyKeyboardMarkup(
    [["1. Porcentaje de ganancias"], ["2. Plataforma de apuestas"],
     ["3. Duda de pick"], ["4. Otra pregunta"]],
    resize_keyboard=True
)

# Estados temporales
dynamic_state = {}

# Normalizar texto
def normalizar(texto):
    texto = texto.lower().strip()
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.effective_user.id)
    dynamic_state.pop(user_id, None)
    await update.message.reply_text("👋 ¿Cómo puedo ayudarte hoy?", reply_markup=main_menu)

# Manejo de mensajes
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.effective_user.id)
    username = update.effective_user.username or "Sin username"
    nombre = update.effective_user.full_name or "Sin nombre"
    text_raw = update.message.text.strip()
    text = normalizar(text_raw)

    # Si está esperando una respuesta personalizada
    if user_id in dynamic_state:
        motivo = dynamic_state.pop(user_id)
        mensaje = (
            f"📩 Nueva duda de cliente:\n"
            f"👤 Nombre: {nombre}\n"
            f"🆔 ID de Telegram: {user_id}\n"
            f"🔗 Usuario: @{username}\n"
            f"📌 Motivo: {motivo}\n"
            f"✉️ Mensaje: {text_raw}"
        )
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=mensaje)
        await update.message.reply_text("Gracias, un administrador te responderá pronto.")
        return

    # OPCIÓN 1: Información del grupo premium
    if "grupo premium" in text:
        registro_url = (
            f"https://api.buclecompany.com/widget/form/K4jL17NuYNDNplEEu22x"
            f"?notrack=true&telegram_id={user_id}"
        )
        await update.message.reply_text(
            "👋 <b>Hola!</b>\n\n"
            "💸 El costo de entrada al grupo es de <b>499 pesos mexicanos</b> (aproximadamente <b>25 USD</b>) mensuales.\n"
            "🎟️ Una vez realizado el pago, se te agrega directamente al grupo premium.\n\n"
            f"📝 Llena este formulario para registrarte y realizar el pago:\n"
            f"<a href='{registro_url}'>{registro_url}</a>\n\n"
            "📬 Una vez completado el formulario, recibirás el acceso al grupo premium:\n"
            "<a href='https://t.me/+8_k_c4DgkbE4M2Ux'>https://t.me/+8_k_c4DgkbE4M2Ux</a>",
            parse_mode="HTML"
        )
        return

    # OPCIÓN 2: Preguntas frecuentes
    elif "preguntas frecuentes" in text:
        await update.message.reply_text("Selecciona una opción:", reply_markup=faq_menu)
        return

    # SUBMENÚ FAQ
    elif "porcentaje de ganancias" in text:
        await update.message.reply_text("📈 *PROMEDIO MENSUAL:* $11,773 ganados u 11.77 unidades ganadas\n💰 *TOTAL GENERAL:* $82,411 ganados u 82.41 unidades ganadas", parse_mode="Markdown")
        return

    elif "plataforma de apuestas" in text:
        await update.message.reply_text("🏦 Usamos principalmente *Bet365* y *Playdoit*, pero puedes usar cualquier casa que permita apuestas a jugadores.", parse_mode="Markdown")
        return

    elif "duda de pick" in text:
        dynamic_state[user_id] = "Duda sobre pick"
        await update.message.reply_text("📝 Por favor, escribe tu duda sobre algún pick.")
        return

    elif "otra pregunta" in text:
        dynamic_state[user_id] = "Otra pregunta general"
        await update.message.reply_text("🗨️ Por favor, escribe tu pregunta.")
        return

    # Cualquier otra entrada
    else:
        await update.message.reply_text("👋 ¿Cómo puedo ayudarte hoy?", reply_markup=main_menu)

# Ejecutar bot
if __name__ == "__main__":
    print("🔄 Iniciando bot en modo polling...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot corriendo correctamente...")
    app.run_polling()
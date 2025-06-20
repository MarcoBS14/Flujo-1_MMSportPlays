import os
from dotenv import load_dotenv
import unicodedata
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

# Menú principal
main_menu = ReplyKeyboardMarkup(
    [["1. Información sobre el grupo premium"], ["2. Preguntas frecuentes"]],
    resize_keyboard=True
)

faq_menu = ReplyKeyboardMarkup(
    [["1. Porcentaje de ganancias"], ["2. Plataforma de apuestas"], ["3. Duda de pick"], ["4. Otra pregunta"]],
    resize_keyboard=True
)

# Estados temporales por usuario
dynamic_state = {}

# Normalizar texto (sin acentos y en minúsculas)
def normalizar(texto):
    texto = texto.lower().strip()
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.effective_user.id)
    dynamic_state.pop(user_id, None)
    await update.message.reply_text("👋 ¿Cómo puedo ayudarte hoy?", reply_markup=main_menu)

# Manejo general
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.effective_user.id)
    text_raw = update.message.text.strip()
    text = normalizar(text_raw)

    # Revisar si está esperando una respuesta específica
    if user_id in dynamic_state:
        motivo = dynamic_state.pop(user_id)
        mensaje = f"📩 Nueva duda:\nID: {user_id}\nMotivo: {motivo}\nMensaje: {text_raw}"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=mensaje)
        await update.message.reply_text("Gracias, un administrador te responderá pronto.")
        return

    # ✅ OPCIÓN 1 — Información grupo premium
    if text.startswith("1. informacion sobre el grupo premium"):
        registro_url = (
            f"https://api.buclecompany.com/widget/form/NzctQhiqWZCkJyHaUtti"
            f"?notrack=true&telegram_id={user_id}"
        )
        await update.message.reply_text(
            "🎯 *Información sobre el grupo premium:*\n\n"
            "✅ Acceso a picks diarios\n"
            "📈 Estrategias con respaldo numérico\n"
            "🤖 Automatización de alertas\n"
            "💬 Comunidad privada en Telegram\n\n"
            "📝 Para solicitar acceso, llena este formulario:\n"
            f"{registro_url}",
            parse_mode="Markdown"
        )
        return

    # ✅ OPCIÓN 2 — Preguntas frecuentes
    elif text.startswith("2. preguntas frecuentes"):
        await update.message.reply_text("Selecciona una opción:", reply_markup=faq_menu)
        return

    # ✅ SUBMENÚ FAQ
    elif text.startswith("1. porcentaje de ganancias"):
        await update.message.reply_text("📊 El porcentaje de ganancias mensual es de aproximadamente 85%.")
        return

    elif text.startswith("2. plataforma de apuestas"):
        await update.message.reply_text("🏟 Usamos principalmente Bet365 y Caliente.mx.")
        return

    elif text.startswith("3. duda de pick"):
        dynamic_state[user_id] = "Duda sobre pick"
        await update.message.reply_text("📝 Por favor, escribe tu duda sobre algún pick.")
        return

    elif text.startswith("4. otra pregunta"):
        dynamic_state[user_id] = "Otra pregunta general"
        await update.message.reply_text("🗨️ Por favor, escribe tu pregunta.")
        return

    # ❓ Cualquier otra entrada
    else:
        await update.message.reply_text("👋 ¿Cómo puedo ayudarte hoy?", reply_markup=main_menu)

# Lanzar el bot
if __name__ == "__main__":
    print("🔄 Iniciando bot en modo polling...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot corriendo correctamente...")
    app.run_polling()
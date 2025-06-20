import os
import requests
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
GHL_API_KEY = os.getenv("GHL_API_KEY")
GHL_BASE_URL = "https://rest.gohighlevel.com/v1"
ADMIN_CHAT_ID = 6130272246

# Clave del campo personalizado
TELEGRAM_FIELD_KEY = "telegram_id"

# Menús
main_menu = ReplyKeyboardMarkup(
    [["1. Información sobre el grupo premium"], ["2. Preguntas frecuentes"]],
    resize_keyboard=True
)

faq_menu = ReplyKeyboardMarkup(
    [["1. Porcentaje de ganancias"], ["2. Plataforma de apuestas"], ["3. Duda de pick"], ["4. Otra pregunta"]],
    resize_keyboard=True
)

# Estados dinámicos
dynamic_state = {}

# Normalizador
def normalizar(texto):
    texto = texto.lower()
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

# Función para registrar contacto y actualizar telegram_id
def registrar_en_ghl(telegram_id: int, email: str, nombre: str = ""):
    headers = {
        "Authorization": f"Bearer {GHL_API_KEY}",
        "Content-Type": "application/json"
    }

    contacto = {
        "email": email,
        "tags": ["Lead interesado"]
    }
    if nombre:
        contacto["firstName"] = nombre

    try:
        # Crear contacto
        print(f"📤 Creando contacto: {email}, nombre: {nombre}")
        create_response = requests.post(f"{GHL_BASE_URL}/contacts/", headers=headers, json=contacto)
        data = create_response.json()

        if create_response.status_code not in [200, 201]:
            print("❌ Error al crear contacto:", create_response.status_code, data)
            return False

        contact_id = data.get("contact", {}).get("id")
        print("🧾 Contact ID recibido:", contact_id)

        if not contact_id:
            print("❌ No se obtuvo el contact_id del nuevo contacto")
            return False

        # Actualizar custom field
        payload = [{
            "fieldKey": TELEGRAM_FIELD_KEY,
            "value": str(telegram_id)
        }]
        update_url = f"{GHL_BASE_URL}/contacts/{contact_id}/customFields"

        print(f"📤 Enviando telegram_id al contacto {contact_id}: {telegram_id}")
        print("🔗 URL:", update_url)
        print("📦 Payload:", payload)

        update_response = requests.put(update_url, headers=headers, json=payload)

        print("📬 Respuesta actualización:", update_response.status_code, update_response.text)
        return update_response.status_code in [200, 201]

    except Exception as e:
        print(f"❌ Error general:", e)
        return False

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.effective_user.id)
    dynamic_state.pop(user_id, None)
    await update.message.reply_text("¡Hola! 👋 ¿Cómo puedo ayudarte hoy?", reply_markup=main_menu)

# Manejo de mensajes
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.effective_user.id)
    text_raw = update.message.text.strip()
    text = normalizar(text_raw)

    if user_id in dynamic_state:
        motivo = dynamic_state.pop(user_id)
        if motivo == "esperando_email":
            email = text_raw
            nombre = update.effective_user.first_name
            print(f"🆔 Registrando usuario con Telegram ID: {user_id}")
            ok = registrar_en_ghl(user_id, email, nombre)
            if ok:
                await update.message.reply_text("✅ Registro exitoso. Gracias por tu interés.")
            else:
                await update.message.reply_text("❌ Ocurrió un error al registrar tus datos.")
            return
        else:
            mensaje = f"📩 Nueva duda:\nID: {user_id}\nMotivo: {motivo}\nMensaje: {text_raw}"
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=mensaje)
            await update.message.reply_text("Gracias, un administrador te responderá pronto.")
            return

    # Menú principal
    if text_raw == "1. Información sobre el grupo premium":
        await update.message.reply_text("Por favor, escribe tu correo electrónico para continuar con tu registro:")
        dynamic_state[user_id] = "esperando_email"

    elif text_raw == "2. Preguntas frecuentes":
        await update.message.reply_text("Selecciona una opción:", reply_markup=faq_menu)

    elif text_raw == "1. Porcentaje de ganancias":
        await update.message.reply_text("El porcentaje de ganancias mensual es de aproximadamente 85%.")

    elif text_raw == "2. Plataforma de apuestas":
        await update.message.reply_text("Usamos principalmente Bet365 y Caliente.mx.")

    elif text_raw == "3. Duda de pick":
        dynamic_state[user_id] = "Duda sobre pick"
        await update.message.reply_text("Escribe tu duda sobre un pick.")

    elif text_raw == "4. Otra pregunta":
        dynamic_state[user_id] = "Otra pregunta general"
        await update.message.reply_text("Por favor, escribe tu pregunta.")

    else:
        await update.message.reply_text("¡Hola! 👋 ¿Cómo puedo ayudarte hoy?", reply_markup=main_menu)

# Iniciar bot
if __name__ == "__main__":
    print("🔄 Iniciando bot en modo polling...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot corriendo correctamente…")
    app.run_polling()
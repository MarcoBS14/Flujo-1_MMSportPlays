from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Función para iniciar el bot y mostrar el ID del usuario
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name

    # Aquí puedes almacenar el ID, por ejemplo en una base de datos o archivo
    print(f"Nuevo usuario: {first_name} (ID: {user_id})")

    await update.message.reply_text(
        f"Hola {first_name}, tu Telegram ID ha sido registrado correctamente."
    )

# También puedes capturar cualquier mensaje si no quieres depender de /start
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text
    print(f"Mensaje recibido de {user_id}: {message}")
    await update.message.reply_text("Gracias por tu mensaje. Ya registramos tu Telegram ID.")

# Punto de entrada
if __name__ == "__main__":
    import os

    # Reemplaza con tu token
    TOKEN = "TU_TOKEN_DE_TELEGRAM"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot corriendo...")
    app.run_polling()
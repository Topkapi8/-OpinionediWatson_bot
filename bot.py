import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ✅ Token direttamente nel codice (come richiesto)
BOT_TOKEN = "7845871925:AAE8PWzG3IRzo-vsX-Dw9htcQ_GwvW0VY5o"

# 🔗 Codici e PDF associati
CODE_TO_FILE = {
   "001": "001.pdf",
   "002": "articolo_distopico_002.pdf",
}

# 💬 Risposta standard
REPLY_STANDARD = (
    "Grazie di averci contattato, questo e' un messaggio automatico , avete mandato un articolo? Lo abbiamo girato il vostro articolo a Watson che, "
    "se lo giudicherà stimolante per la comunità, lo pubblicherà con la sua risposta."
)

# 📬 Gestione dei messaggi
ADMIN_ID = 1106121694  # <-- Sostituisci con il tuo vero ID Telegram

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.strip() if update.message.text else None
    print(f"📩 Messaggio ricevuto: {text}")

    # ✉️ Invia copia del messaggio all’amministratore
    admin_message = f"📩 Nuovo messaggio da @{user.username or 'utente_sconosciuto'} (ID: {user.id}):\n{text}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)

    # 🔍 Controllo del codice
    if text and text in CODE_TO_FILE:
        file_path = CODE_TO_FILE[text]
        print(f"📂 Codice riconosciuto, file associato: {file_path}")
        try:
            with open(file_path, 'rb') as f:
                await update.message.reply_document(document=f)
                print("✅ File inviato correttamente.")
        except FileNotFoundError:
            await update.message.reply_text("❌ File non trovato.")
    else:
        await update.message.reply_text(REPLY_STANDARD)


# 🚀 Avvio del bot
def main():
    print("🤖 Avvio del bot OpinioneDistopica...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()

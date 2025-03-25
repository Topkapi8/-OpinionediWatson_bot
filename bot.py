import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters
)

# 🔐 Token del bot Telegram
BOT_TOKEN = "7845871925:AAE8PWzG3IRzo-vsX-Dw9htcQ_GwvW0VY5o"

# 🧑‍💼 ID Telegram dell'amministratore
ADMIN_ID = 1106121694  # Assicurati che sia un numero, senza virgolette

# 📚 Mappa codici -> file
CODE_TO_FILE = {
    "001": "001 - Canale di Panama@DistopiaQuotidiana.pdf",
    "002": "articolo_distopico_002.pdf",
}

# 🧠 Messaggio standard
REPLY_STANDARD = (
    "Grazie di averci contattato, abbiamo girato il vostro articolo a Watson che, "
    "se lo giudicherà stimolante per la comunità, lo pubblicherà con la sua risposta."
)

# 📨 Funzione per gestire tutti i messaggi (testo + file)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.strip() if update.message.text else None

    # 📌 Se è un documento (file inviato)
    if update.message.document:
        document = update.message.document
        file = await context.bot.get_file(document.file_id)

        caption = f"📌 Documento ricevuto da @{user.username or 'utente_sconosciuto'} (ID: {user.id})\nNome file: {document.file_name}"
        await context.bot.send_document(chat_id=ADMIN_ID, document=document.file_id, caption=caption)
        await update.message.reply_text(REPLY_STANDARD)
        return

    # 📢 Notifica all'amministratore per i messaggi di testo
    admin_message = f"📩 Nuovo messaggio da @{user.username or 'utente_sconosciuto'} (ID: {user.id}):\n{text}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)

    # 🔍 Verifica se il messaggio è un codice valido
    if text and text in CODE_TO_FILE:
        file_path = CODE_TO_FILE[text]
        try:
            with open(file_path, 'rb') as f:
                await update.message.reply_document(document=f)
        except FileNotFoundError:
            await update.message.reply_text("❌ Il file associato a questo codice non è stato trovato.")
    else:
        await update.message.reply_text(REPLY_STANDARD)

# ✉️ Comando /reply per far rispondere il bot a un utente specifico
async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_id = update.effective_user.id
    print(f"[DEBUG] Admin ID: {ADMIN_ID} - Utente: {sender_id}")

    if str(sender_id) != str(ADMIN_ID):
        await update.message.reply_text("⛔️ Non hai il permesso per usare questo comando.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("❗ Usa il comando così: /reply <user_id> <messaggio>")
        return

    try:
        target_user_id = int(context.args[0])
        reply_text = ' '.join(context.args[1:])
        await context.bot.send_message(chat_id=target_user_id, text=reply_text)
        await update.message.reply_text("✅ Messaggio inviato con successo.")
    except Exception as e:
        await update.message.reply_text(f"❌ Errore: {e}")

# 🚀 Avvio del bot
def main():
    print("🤖 Avvio del bot OpinioneDistopica...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("reply", reply_command))
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    app.run_polling()

if __name__ == '__main__':
    main()

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# 🔐 Inserisci il tuo TOKEN
BOT_TOKEN = 'INSERISCI_IL_TUO_TOKEN_QUI'

# 📦 Codici e file associati (aggiungili nella cartella dove gira lo script)
CODE_TO_FILE = {
    "001": "articolo_distopico_001.pdf",
    "A23": "opinione_A23.pdf",
    "distopico5": "distopia_5.pdf"
}

# 🧠 Risposta standard
REPLY_STANDARD = (
    "Grazie di averci contattato, abbiamo girato il vostro articolo a Watson che, "
    "se lo giudicherà stimolante per la comunità, lo pubblicherà con la sua risposta."
)

# 📬 Gestione dei messaggi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip() if update.message.text else None

    if text and text in CODE_TO_FILE:
        file_path = CODE_TO_FILE[text]
        try:
            await update.message.reply_document(document=open(file_path, 'rb'))
        except FileNotFoundError:
            await update.message.reply_text("Il file associato a questo codice non è stato trovato.")
    else:
        await update.message.reply_text(REPLY_STANDARD)

# 🚀 Avvio del bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.Document.ALL, handle_message))
    print("Bot in esecuzione...")
    app.run_polling()

if __name__ == '__main__':
    main()

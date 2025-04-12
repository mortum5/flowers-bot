import os
import tempfile
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from flower_generator import generate_image

logging.basicConfig(level=logging.INFO)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome! Use /generate <description in Russian> to generate a realistic flower bouquet image."
    )

def generate(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Please provide a description in Russian. Example: /generate красивый букет роз")
        return
    # Combine command arguments into a query.
    query = " ".join(context.args)
    update.message.reply_text("Generating image, please wait...")
    
    # Use a temporary file to save the generated image.
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        image_path = tmp_file.name
    
    try:
        generate_image(query, output_path=image_path)
        update.message.reply_photo(photo=open(image_path, "rb"))
    except Exception as e:
        logging.error("Error generating image: %s", e)
        update.message.reply_text("Sorry, there was an error generating the image.")
    finally:
        # Clean up the temporary file.
        if os.path.exists(image_path):
            os.remove(image_path)

def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: Please set the TELEGRAM_BOT_TOKEN environment variable.")
        return
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("generate", generate))
    
    print("Bot is starting...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

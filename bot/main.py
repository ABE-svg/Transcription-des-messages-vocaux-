import os
import asyncio
import tempfile

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes,CommandHandler


from .utils import *

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not found in environment")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #this bot has only one command : bot introduction
    user = update.effective_user
    name = (user.first_name or "").strip() if user else ""
    
    if name:
        greeting = f"""Hi {name}, welcome to the Voice-to-Text bot.
Send a Telegram voice message and I’ll convert it to text. 
If it’s in another language, I’ll translate it for you as well."""
    else:
        greeting = """Hi, welcome to the Voice-to-Text bot.
Send a Telegram voice message and I’ll convert it to text. 
If it’s in another language, I’ll translate it for you as well."""
        
    await update.message.reply_text(greeting)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #get user language 
    user_lang = update.effective_user.language_code
    #append temporary message assuring user that the file is being processed
    status_msg = await update.message.reply_text(
        "Processing voice message..."
    )

    #get voice message
    file = await context.bot.get_file(update.message.voice.file_id)

    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
        temp_path = tmp.name
        await file.download_to_drive(temp_path)

    #try to transcribe audio file 
    try:
        result = await transcribe_audio(temp_path)
    except Exception as e:
        #if error then likely reason : tokens open ai exceeded
        try:
            os.remove(temp_path)
        except:
            pass

        await status_msg.delete()

        await update.message.reply_text(
            "Transcription service unavailable.\n"
            "Likely reason: OpenAI credits exhausted or API error."
        )
        return

    #if no error then delete message  "Processing voice message..." and delete temp audio file 
    try:
        os.remove(temp_path)
    except Exception:
        pass
    
    await status_msg.delete()
    # get results 

    text = result["text"]

    whisper_lang_name = (result["language"] or "").lower()
    detected_lang_code = LANG_NAME_TO_CODE.get(whisper_lang_name)

    # always send transcription results 
    await update.message.reply_text(
        f"Language: {whisper_lang_name}\n\n{text}"
    )

    #if whisper_lang_name id not supported by LANG_NAME_TO_CODE then return 
    if not detected_lang_code:
        return

    # if audio language = user language then return 
    if detected_lang_code == user_lang:
        return

    #if audio language != user language then translate also 
    try:
        translated = await translator(text, user_lang)
    except Exception as e:
        await update.message.reply_text(
            "Translation unavailable.\n"
            "Likely reason: OpenAI credits exhausted or API error."
        )
        return

    await update.message.reply_text(
        f"Translated to {user_lang}:\n\n{translated}"
    )


async def ignore_others(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    do nothing if other then voice  message formats are sent by user 
    """
    return


def main():
     
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(~filters.VOICE, ignore_others))

    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()

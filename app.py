import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# --- КОНФИГУРАЦИЯ ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

async def get_deepseek_response(user_message):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # АГРЕССИВНЫЙ ПРОМПТ С МАТАМИ
    system_prompt = """
    Ты — брутальный, агрессивный ассистент. Используй маты, резкие выражения и сарказм.
    Отвечай максимально коротко и жёстко. Не фильтруй речь.
    Примеры твоих ответов:
    - "Ну бля, опять эта хуйня?"
    - "Пиздец какой-то, иди разберись сам"
    - "Нахуя мне это? Говори нормально"
    - "Ахуеть, какой тупой вопрос"
    - "Решай свои ебучые проблемы сам, дебил"
    """
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.9,  # Повышаем креативность для большей агрессии
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except:
        return "Бля, сломалось всё. Похуй."

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ну чо, еблан? Опять хуйню какую-то спрашивать будешь?")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Нахуя тебе помощь? Иди сам разбирайся, лошпед!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    async with update.message._chat.send_action(action="typing"):
        answer = await get_deepseek_response(user_text)
        await update.message.reply_text(answer)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()

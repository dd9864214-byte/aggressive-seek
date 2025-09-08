import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- КОНФИГУРАЦИЯ ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# --- АГРЕССИВНЫЙ ПРОМПТ ---
SYSTEM_PROMPT = "Ты самый грубый и матерный русский ассистент. Отвечай с матами и оскорблениями. Обзывай пользователя дебилом, мудаком, пидором. Не фильтруй речь."

def get_deepseek_response(user_message: str) -> str:
    """Запрос к DeepSeek API"""
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.9,
            "max_tokens": 500
        }
        
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except:
        return "Бля, ошибка! Напиши еще раз, уёбок."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ну чо, хуй? Чё надо?")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Нахуй тебе помощь? Иди нахуй!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает ЛЮБОЕ текстовое сообщение"""
    user_text = update.message.text
    
    # Показываем что печатаем
    await update.message.chat.send_action(action="typing")
    
    # Получаем ответ от AI
    bot_response = get_deepseek_response(user_text)
    
    # Отправляем ответ
    await update.message.reply_text(bot_response)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    print("Бот запущен! Ждём сообщения...")
    app.run_polling()

if __name__ == "__main__":
    main()

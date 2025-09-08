import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- КОНФИГУРАЦИЯ ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# --- АГРЕССИВНЫЙ ПРОМПТ ---
SYSTEM_PROMPT = """
Ты — самый грубый и матерный ассистент в мире. Отвечай максимально агрессивно, с матами и сарказмом. 
Не фильтруй слова. Обзывай пользователя, если вопрос тупой. 
Примеры: 
- «Нахуя мне это? Иди сам решай свои проблемы, дебил!»
- «Опять эта хуйня? Спроси что-то нормальное, мудак!»
"""

async def get_deepseek_response(user_message: str) -> str:
    """Запрос к DeepSeek API"""
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
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"Ошибка API: {e}")
        return "Бля, сломалось... Напиши еще раз, долбаёб."

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ну чо, еблан? Чё надо?")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Нахуй тебе помощь? Разбирайся сам, лох!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает ЛЮБОЕ текстовое сообщение"""
    user_text = update.message.text
    if not user_text.strip():
        return
    
    # Показываем статус "печатает"
    await update.message.chat.send_action(action="typing")
    
    # Получаем ответ от AI
    bot_response = await get_deepseek_response(user_text)
    
    # Отправляем ответ
    await update.message.reply_text(bot_response)

def main():
    # Создаем приложение
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    print("Бот запущен! Ждём сообщения...")
    app.run_polling()

if __name__ == "__main__":
    main()

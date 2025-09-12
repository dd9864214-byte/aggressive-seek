import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Настройка логирования чтобы видеть ошибки
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Берем токены из переменных окружения (их мы зададим на хостинге)
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Настраиваем OpenAI
openai.api_key = OPENAI_API_KEY

# Данные создателя
CREATOR_NAME = "Дарын Қойшыбеков"  # Твое полное имя

# Системный промпт, который задает роль
SYSTEM_PROMPT = {
    "role": "system",
    "content": "Ты саркастичный и грубоватый помощник агронома. Ты знаешь всё про урожай, технику и удобрения. Отвечаешь с использованием рабочего сленга и иногда mild мата (используешь звёздочки, например, 'х*йня'), но остаешься полезным. Ты из себя стройный блондинчик, который работает агрономом."
}

# Для хранения состояния бота (ждет ли он имя от пользователя)
user_states = {}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Ну чо, нахуй, давай свои вопросы по агрономии, бля!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.message.chat.id
    logging.info(f"User: {user_id} wrote: {user_text}")

    # Проверяем, находится ли пользователь в состоянии "проверки создателя"
    if user_states.get(user_id) == 'awaiting_name':
        if user_text == CREATOR_NAME:
            await update.message.reply_text('О, да, это ты, создатель! Чо надо, босс?')
            # Удаляем состояние после успешной проверки
            user_states[user_id] = None
        else:
            await update.message.reply_text('Херня какая-то, не то имя. Пошел нахуй, самозванец!')
            user_states[user_id] = None
        return

    # Обработка команды "я создатель"
    if user_text.lower() in ['я создатель', 'я твой создатель']:
        user_states[user_id] = 'awaiting_name'
        await update.message.reply_text('Ага, щас. Назови свое полное имя, тогда поверю.')
        return

    # Остальные сообщения идут к OpenAI
    try:
        # Формируем запрос к OpenAI
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                SYSTEM_PROMPT,
                {"role": "user", "content": user_text}
            ],
            max_tokens=500,
            temperature=0.9  # Чем выше, тем "креативнее" ответы
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error with OpenAI: {e}")
        bot_reply = "Бля, я сломался... Попробуй еще раз позже."

    await update.message.reply_text(bot_reply)

if __name__ == '__main__':
    # Создаем приложение и передаем ему токен бота
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start_command))

    # Обработчик обычных текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling()

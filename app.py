import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- ЛОГИ ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# === НАСТРОЙКА ===
CENZORED = False  # 👉 False = мат как есть, True = замена звёздочками

# --- СЛОВА ДЛЯ ЦЕНЗУРЫ ---
BAD_WORDS = {
    "блять", "сука", "нахуй", "пиздец", "ебать", "хуй", "даун", "мудак"
}

def censor(text: str) -> str:
    if not CENZORED:
        return text
    out = text
    for w in BAD_WORDS:
        out = out.replace(w, w[0] + "*"*(len(w)-1))
    return out

# --- ШАБЛОНЫ ОТВЕТОВ ---
AGRO_TEMPLATES = [
    "Чё ты несёшь, {user}? Блять, это же пиздец какой-то.",
    "Да ты заебал уже, {user}, думать не пробовал?",
    "{user}, нахуй такие тупые вопросы вообще задавать?",
    "Серьёзно? Ебать, я в ахуе с тебя.",
    "Пиздец, {user}, ты прям как даун сейчас выглядишь.",
    "Хуйню написал и радуется… Браво!",
    "Сука, {user}, ну это даже объяснять стыдно.",
    "Короче, иди нахуй с такими темами.",
    "Блять, ну ты и мудак, {user}.",
    "Ебать мой хуй… Я в шоке с этого."
]

START_MSG = [
    "Я — AGRO BOT. Буду отвечать жёстко, без соплей и по хардкору. 🔥",
    "Здарова, {user}. Готовь жопу — тут будет грязно. 😈"
]

HELP_MSG = (
    "Команды:\n"
    "/start — запуск\n"
    "/help — помощь\n\n"
    "Просто пиши что угодно — и я выдам тебе агрессивный ответ."
)

# --- ХЭНДЛЕРЫ ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "ебать кто"
    msg = random.choice(START_MSG).format(user=user)
    await update.message.reply_text(censor(msg))

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(censor(HELP_MSG))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "ебать кто"
    template = random.choice(AGRO_TEMPLATES)
    reply = template.format(user=user)
    await update.message.reply_text(censor(reply))

# --- MAIN ---
def main():
    import os
    TOKEN = os.getenv("TG_BOT_TOKEN")  # сюда вставь свой токен
    if not TOKEN:
        print("❌ Установи TG_BOT_TOKEN в переменных окружения или пропиши строкой в коде")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🔥 AGRO BOT запущен. Жди хардкора!")
    app.run_polling()

if __name__ == "__main__":
    main()

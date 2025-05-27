import logging
import json
import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

QUEST = [
    # ... (твій список завдань без змін)
]

PROGRESS_FILE = 'user_progress.json'

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_progress(progress):
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f)

user_progress = load_progress()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    user_progress[user_id] = 0
    save_progress(user_progress)
    await send_quest_point(update, context)

async def send_quest_point(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    step = user_progress.get(user_id, 0)
    if step < len(QUEST):
        point = QUEST[step]
        hint = f"\n\n📌 _Підказка:_ {point['hint']}" if 'hint' in point else ""
        message = f"{point['title']}\n\n{point['text']}\n\nЗавдання: {point['question']}{hint}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="Markdown")
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                "🎉 Вітаю! Ви пройшли весь квест 'Код Ейнштейна'.\n\n"
                "Ви відкрили не просто відповіді — ви відчули дух пошуку, де кожна загадка — це крок до розуміння глибин світу і себе.\n"
                "Як колись Ейнштейн казав, «Уява важливіша за знання», і саме уява веде нас за межі очевидного.\n\n"
                "Нехай цей шлях надихає вас не боятись питати, шукати і відкривати нове — адже справжня мудрість починається там, де закінчується звичне."
            )
        )

def check_answer(user_answer, expected_answers):
    normalized_user_answer = ''.join(user_answer.lower().split())
    normalized_expected = [''.join(ans.lower().split()) for ans in expected_answers]

    if normalized_user_answer in normalized_expected:
        return True

    # Спеціальний випадок для цифр (як 1884) — перевірка з урахуванням чисел
    for ans in expected_answers:
        if re.search(r'\b' + re.escape(ans.lower()) + r'\b', user_answer.lower()):
            return True
    return False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    step = user_progress.get(user_id, 0)
    if step < len(QUEST):
        point = QUEST[step]
        user_answer = update.message.text.strip()

        logging.info(f"User answer: '{user_answer}' | Step: {step}")

        if check_answer(user_answer, point["answer"]):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Вірно!")
            user_progress[user_id] = step + 1
            save_progress(user_progress)
            await send_quest_point(update, context)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Невірно. Спробуй ще раз.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Ви вже пройшли весь квест!")

if __name__ == '__main__':
   ApplicationBuilder().token("7222439087:AAF4nAy9vsmr9TkIsVqojFnk8oevXJSKL-s").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling()

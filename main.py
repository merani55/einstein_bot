from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import re

# Дані квесту
QUEST_POINTS = [
    {
        "text": (
            "Точка 1 — Початок шляху\n\n"
            "«У кожній формулі — історія. У кожній вулиці — секрет.»\n\n"
            "Завдання: Знайди вулицю, де починається наш квест, на честь великого вченого. "
            "Назви її точно."
        ),
        "answer": "müllerstraße",
        "hint": "Це вулиця, де жив Ейнштейн у Мюнхені."
    },
    {
        "text": (
            "Точка 2 — Інститут оптики\n\n"
            "«Світло — це найшвидший посланець.»\n\n"
            "Завдання: Назви колишнє місце Інституту оптики в Мюнхені."
        ),
        "answer": "gabelsbergerstraße",
        "hint": "Інститут знаходився на честь видатного німецького лінгвіста, на вулиці, що носить його прізвище."
    },
    {
        "text": (
            "Точка 3 — Гімназія Лютпольда\n\n"
            "«Тут формується майбутнє — у стінах, де навчався геній.»\n\n"
            "Завдання: Як називається гімназія, де навчався Ейнштейн?"
        ),
        "answer": ["luitpold-gymnasium", "luitpold gymnasium"],
        "hint": "Назва містить 'luitpold' і 'gymnasium'."
    },
    # ... інші точки ...
    {
        "text": (
            "Точка 9 — Місце рівноваги\n\n"
            "«Математика привела мене до ринку — місця, де все збалансовано.»\n\n"
            "Завдання: Тут можна знайти симетрію в хаосі. Продукти і формули тут поєднуються в гармонії. "
            "Ейнштейн любив порядок, а тут — його жива форма. Відгадай назву цього історичного місця Мюнхена.\n\n"
            "📌 _Підказка (за запитом):_ В центрі міста, де запахи і кольори творять симфонію, починаються та закінчуються подорожі."
        ),
        "answer": "viktualienmarkt",
        "hint": "В центрі міста, де запахи і кольори творять симфонію, починаються та закінчуються подорожі."
    }
]

# Збереження стану кожного гравця: user_id -> індекс поточної точки
user_progress = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_progress[user_id] = 0
    await update.message.reply_text(
        "Вітаємо у квесті «Код Ейнштейна»! Починаємо з першої точки.\n\n" +
        QUEST_POINTS[0]["text"]
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_progress:
        await update.message.reply_text("Будь ласка, почніть квест командою /start")
        return

    current_index = user_progress[user_id]
    if current_index >= len(QUEST_POINTS):
        await update.message.reply_text("Ви пройшли весь квест! Вітаємо!")
        return

    user_answer = update.message.text.lower().strip()

    # Перевірка відповіді — враховує варіанти відповідей (список або рядок)
    correct_answer = QUEST_POINTS[current_index]["answer"]
    if isinstance(correct_answer, list):
        is_correct = any(user_answer == ans for ans in correct_answer)
    else:
        is_correct = (user_answer == correct_answer)

    # Додатково - можна додати нормалізацію (видалення пробілів, знаків)
    def normalize(s):
        return re.sub(r"[\s\-]", "", s.lower())
    normalized_answer = normalize(user_answer)
    if isinstance(correct_answer, list):
        is_correct = any(normalize(ans) == normalized_answer for ans in correct_answer)
    else:
        is_correct = (normalize(correct_answer) == normalized_answer)

    if is_correct:
        user_progress[user_id] += 1
        if user_progress[user_id] == len(QUEST_POINTS):
            await update.message.reply_text("Вітаємо! Ви пройшли весь квест!")
        else:
            next_point_text = QUEST_POINTS[user_progress[user_id]]["text"]
            await update.message.reply_text(
                "Вірно! " +
                next_point_text
            )
    else:
        await update.message.reply_text(
            "Неправильна відповідь. Спробуйте ще раз або напишіть 'підказка' для допомоги."
        )

async def hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_progress:
        await update.message.reply_text("Будь ласка, почніть квест командою /start")
        return

    current_index = user_progress[user_id]
    if current_index >= len(QUEST_POINTS):
        await update.message.reply_text("Ви пройшли весь квест, підказки вже не потрібні.")
        return

    hint_text = QUEST_POINTS[current_index]["hint"]
    await update.message.reply_text(f"Підказка: {hint_text}")

def main():
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN_HERE").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("підказка", hint))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()



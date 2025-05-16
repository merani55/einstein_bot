from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Дані квесту: завдання і відповіді
quest_points = [
    {
        "description": "Завдання 1: Тут можна знайти симетрію в хаосі. Продукти і формули тут поєднуються в гармонії. Ейнштейн любив порядок, а тут — його жива форма. Відгадай назву цього історичного місця.",
        "answer": "suuapvnga"
    },
    {
        "description": "Завдання 2: Машини і люди, боротьба за інновації. Тут поєднались креативність і техніка. Відгадай, де це місце.",
        "answer": "man versus machine"
    },
    {
        "description": "Завдання 3: Центральний ринок з різноманіттям смаків і кольорів. Тут можна відчути дух міста. Назва цього місця?",
        "answer": "viktualienmarkt"
    },
    {
        "description": "Завдання 4: Місце навчання з великою історією, де освіта і традиції переплітаються. Назва гімназії?",
        "answer": "luitpold-gymnasium"
    }
]

# Прогрес користувачів: user_id -> індекс поточної точки квесту
user_progress = {}

# Підказки для кожної точки
hints = [
    "Підказка до завдання 1: Подумай про симетрію і порядок у науці.",
    "Підказка до завдання 2: Машини vs Люди — це назва.",
    "Підказка до завдання 3: Місце з ринком і смаколиками в центрі.",
    "Підказка до завдання 4: Гімназія з німецьким ім’ям, пов’язана з освітою."
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_progress[user_id] = 0
    await update.message.reply_text(
        "Вітаємо в квесті 'Код Ейнштейна'! Починаємо з першого завдання:\n\n"
        + quest_points[0]["description"]
    )

async def hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_progress:
        await update.message.reply_text("Спочатку почніть квест командою /start")
        return
    index = user_progress[user_id]
    await update.message.reply_text(hints[index])

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_progress:
        await update.message.reply_text("Будь ласка, почніть квест командою /start")
        return

    text = update.message.text.lower().strip()

    # Якщо користувач просить підказку словом "підказка"
    if text == "підказка":
        await hint(update, context)
        return

    current_index = user_progress[user_id]
    correct_answer = quest_points[current_index]["answer"]

    # Особливість для luitpold-gymnasium — приймаємо також без дефісу
    if correct_answer == "luitpold-gymnasium":
        if text == "luitpold-gymnasium" or text == "luitpold gymnasium":
            user_progress[user_id] += 1
            await update.message.reply_text("Відповідь правильна! Ви завершили квест. Вітаємо!")
        else:
            await update.message.reply_text("Невірна відповідь. Спробуйте ще раз або надішліть 'підказка'.")
        return

    if text == correct_answer:
        user_progress[user_id] += 1
        if user_progress[user_id] >= len(quest_points):
            await update.message.reply_text("Відповідь правильна! Ви завершили квест. Вітаємо!")
        else:
            next_task = quest_points[user_progress[user_id]]["description"]
            await update.message.reply_text(f"Відповідь правильна!\n\nНаступне завдання:\n{next_task}")
    else:
        await update.message.reply_text("Невірна відповідь. Спробуйте ще раз або надішліть 'підказка'.")

def main():
    # Вставте сюди свій токен
    TOKEN = "ВАШ_ТЕЛЕГРАМ_ТОКЕН"

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hint", hint))  # Команда для підказки

    # Обробник текстових повідомлень
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()




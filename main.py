from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Питання, відповіді і підказки
QUESTIONS = [
    {
        "question": "Питання 1: Хто винайшов теорію відносності?",
        "answer": "айнштайн",
        "hint": "Це ім'я починається на 'А'."
    },
    {
        "question": "Питання 2: Який колір неба?",
        "answer": "блакитний",
        "hint": "Це колір моря в ясний день."
    },
    {
        "question": "Питання 3: Скільки планет у Сонячній системі?",
        "answer": "вісім",
        "hint": "Більше ніж сім, менше ніж дев'ять."
    }
]

# Словник, де ключ — user_id, а значення — індекс поточного питання
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = 0  # Починаємо з першого питання
    await update.message.reply_text(
        "Вітаю в квесті! Ось твоє перше питання:\n" + QUESTIONS[0]["question"]
    )

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_states:
        await update.message.reply_text("Напишіть /start, щоб почати гру.")
        return

    current_index = user_states[user_id]
    user_answer = update.message.text.lower().strip()

    correct_answer = QUESTIONS[current_index]["answer"]

    if user_answer == correct_answer:
        # Правильна відповідь
        current_index += 1
        if current_index == len(QUESTIONS):
            await update.message.reply_text("Вітаю! Ви відповіли на всі питання!")
            del user_states[user_id]  # Скидаємо стан користувача, бо гра завершена
        else:
            user_states[user_id] = current_index
            await update.message.reply_text(
                f"Правильно! Ось наступне питання:\n{QUESTIONS[current_index]['question']}"
            )
    else:
        # Неправильна відповідь
        await update.message.reply_text("Неправильно. Спробуйте ще раз або напишіть /pidkazka для підказки.")

async def hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_states:
        await update.message.reply_text("Напишіть /start, щоб почати гру.")
        return

    current_index = user_states[user_id]
    hint_text = QUESTIONS[current_index]["hint"]
    await update.message.reply_text(f"Підказка: {hint_text}")

def main():
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("pidkazka", hint))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

    application.run_polling()

if __name__ == "__main__":
    main()

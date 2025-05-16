from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

QUESTIONS = [
    {
        "question": "Точка 1 — Початок\n\n«Все має початок — навіть нескінченність.»\n\nЗавдання: Назви вулицю, з якої починається наш маршрут, де і кава, і філософія зустрічаються під одним дахом.\n\n📌 _Підказка:_ Назва вулиці починається на М і має подвійне “л”.",
        "answer": "мюллерштрассе"
    },
    {
        "question": "Точка 2 — Оптика мислення\n\n«Світло — це не просто хвиля. Це ідея.»\n\nЗавдання: Знайди будівлю, де досліджували світло і теорії простору. Там працювали ті, хто бачив глибше за інших.\n\n📌 _Підказка:_ Це інститут, що має в назві слово «оптика».",
        "answer": "інститут оптики"
    },
    {
        "question": "Точка 3 — Гімназія знань\n\n«Освіта — це те, що залишається, коли все вивчене забуто.»\n\nЗавдання: Назви тип школи, де вчився юний Ейнштейн, поруч із старими мурами.\n\n📌 _Підказка:_ Це гімназія, названа на честь поета або філософа.",
        "answer": "людвігсгімназія"
    }
]

user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = 0
    await update.message.reply_text("🔐 Вітаю в квесті «Код Ейнштейна»!\n\n" + QUESTIONS[0]["question"])

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip().lower()

    if user_id not in user_states:
        await update.message.reply_text("Напишіть /start, щоб почати гру.")
        return

    idx = user_states[user_id]
    if text == QUESTIONS[idx]["answer"]:
        idx += 1
        if idx == len(QUESTIONS):
            await update.message.reply_text("🎉 Вітаю! Ви відповіли на всі завдання та розгадали Код Ейнштейна!")
            del user_states[user_id]
        else:
            user_states[user_id] = idx
            await update.message.reply_text("✅ Правильно!\n\n" + QUESTIONS[idx]["question"])
    else:
        await update.message.reply_text("❌ Неправильно. Спробуйте ще раз або прочитайте уважно підказку у завданні.")

def main():
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

    application.run_polling()

if __name__ == "__main__":
    main()

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = "ТВОЙ_ТОКЕН_ТУТ"

# Структура квесту: кожна точка — це dict з завданням, правильною відповіддю і підказкою
QUEST_POINTS = [
    {
        "task": "Завдання 1:\nТут можна знайти симетрію в хаосі. Продукти і формули тут поєднуються в гармонії. Ейнштейн любив порядок, а тут — його жива форма. Відгадай назву цього історичного місця.",
        "answer": "suapvnga",
        "hint": "Це місце починається на 's' і пов’язане з наукою."
    },
    {
        "task": "Завдання 2:\nІнститут оптики — місце, де світло стає зрозумілішим. Як називається ця будівля, де починається твій шлях у світло знань?",
        "answer": "institut optics",
        "hint": "Відповідь англійською, два слова."
    },
    {
        "task": "Завдання 3:\nЦя гімназія виховала багатьох геніїв. Відгадай її назву (приймається з рискою і без):",
        "answer_variants": ["luitpold-gymnasium", "luitpold gymnasium"],
        "hint": "Назва починається на 'luitpold' і містить слово 'gymnasium'."
    },
    {
        "task": "Завдання 4:\nMan versus Machine — битва ідей та технологій. Відгадай назву цього унікального місця.",
        "answer": "man versus machine",
        "hint": "Три слова, про конфлікт."
    },
    {
        "task": "Завдання 5:\nРинок, де можна знайти все — від спецій до історії. Як називається це серце Мюнхена?",
        "answer": "viktualienmarkt",
        "hint": "Назва починається на 'viktualien'."
    }
]

# Для зберігання стану кожного користувача (індекс точки і кількість підказок)
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = {"point": 0, "hints_used": 0}
    await update.message.reply_text(
        "Вітаю! Починаємо квест.\n" + QUEST_POINTS[0]["task"]
    )

async def hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = user_states.get(user_id)
    if not state:
        await update.message.reply_text("Спершу напишіть /start для початку квесту.")
        return
    point = state["point"]
    if point >= len(QUEST_POINTS):
        await update.message.reply_text("Квест завершено, підказок немає.")
        return
    hint_text = QUEST_POINTS[point]["hint"]
    await update.message.reply_text(f"Підказка: {hint_text}")
    state["hints_used"] += 1

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.lower().strip()
    state = user_states.get(user_id)
    if not state:
        await update.message.reply_text("Спершу напишіть /start для початку квесту.")
        return

    point = state["point"]
    if point >= len(QUEST_POINTS):
        await update.message.reply_text("Квест вже завершено. Дякую, що грали!")
        return

    current_point = QUEST_POINTS[point]

    # Перевірка відповіді
    correct = False
    if "answer" in current_point:
        if text == current_point["answer"]:
            correct = True
    elif "answer_variants" in current_point:
        if text in current_point["answer_variants"]:
            correct = True

    if correct:
        state["point"] += 1
        state["hints_used"] = 0
        if state["point"] == len(QUEST_POINTS):
            await update.message.reply_text("Вітаємо! Ви пройшли весь квест!")
        else:
            next_task = QUEST_POINTS[state["point"]]["task"]
            await update.message.reply_text(f"Правильно!\n{next_task}")
    else:
        await update.message.reply_text("Неправильна відповідь. Спробуйте ще або напишіть /підказка")

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("підказка", hint))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()

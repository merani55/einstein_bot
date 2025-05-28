import logging
import json
import os
import unicodedata
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
def normalize_text(text):
    text = text.strip().lower()
    text = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in text if not unicodedata.combining(c)])
QUEST = [
    {
        "title": "Точка 1 — Послання світла",
        "text": "«У темряві світло ховається за трьома кроками назад.»\n«Розшифруй послання, що стоїть на порозі нових знань.»\n\nЗашифрований текст: `Khoor, Zruog!`",
        "question": "Розшифруй цей текст за шифром Цезаря (зсув на 3 літери назад).",
        "hint": "Подумай про того, хто шукав світло у лінзах і променях.",
        "answer": ["Hello, World!"]
    },
    {
        "title": "Точка 2 — Скляне обличчя науки",
        "text": "«Інтелект — це не знання, а уява.» — А. Ейнштейн\n«Світло відкриває те, що приховано у темряві.»",
        "question": "Підійди до будинку 44 по вулиці Müllerstraße і відгадай, що це було за місце, де фізика ставала мистецтвом світла. Колись тут шліфували лінзи, сьогодні — це будівля зі скляним обличчям. ",
        "hint": "В цьому місці працювали над законами оптики, і воно досі служить науці на вулиці, що колись знала ім’я лінзи.",
        "answer": ["інститут оптики"]
    },
    {
        "title": "Точка 3 — Адреса генія",
        "text": "«Будинок, у якому думки вперше набували форми...\"",
        "question": "Місце, де юний Ейнштейн жив зі своєю родиною, зберігає спокій і сьогодні. Його адреса має число, подільне на 3, 6 і 9. Назва вулиці починається на \"М\" і нагадує про млин.",
        "hint": "Назва вулиці має щось спільне зі словом \"Mühle\".",
        "answer": ["müllerstrasse 54", "mullerstrasse 54", "muellerstrasse 54"]
    },
    {
        "title": "Точка 4 — Місце освіти",
        "text": "«Основа кожного відкриття — фундаментальні знання.»",
        "question": "(47×40)+(4×2) — обчисли та згадай, у якому році Альберт вступив до класичної школи.",
        "hint": "Місто залишило слід у серці юного Ейнштейна саме в цей рік.",
        "answer": ["1888"]
    },
    {
        "title": "Точка 5 — Творча перерва",
        "text": "«У каві — думки, у шумі — натхнення.»",
        "question": "В цій кав’ярні, назва якої звучить наче слово з Гренландії, можна відпочити, перш ніж рушити далі. Її назва починається на \"S\" і містить повтор літери \"а\".",
        "hint": "Вимов цю назву як спів крижаного птаха. Сама назва нічого не означає, але звучить, як з іншого світу.",
        "answer": ["suuapinga"]
    },
    {
        "title": "Точка 6 — Гуманітарна гармонія",
        "text": "«Навіть у музиці чисел є фальшиві ноти.»",
        "question": "З яких двох предметів у Ейнштейна були найгірші оцінки в гімназії?",
        "hint": "Вони — корінь філософії та науки. Їх вивчають ще зі шкільної лави в Європі.",
        "answer": ["латина, грецька"]
    },
    {
        "title": "Точка 7 — Битва розумів",
        "text": "«Машини не мислять, але ми змушуємо їх змагатися.»\n«Уява важливіша за знання, бо знання — обмежені.» — А. Ейнштейн",
        "question": "У Мюнхені є місце, де кава вариться як за формулами, а процес нагадує змагання — бариста проти автомата. Тут людський дотик бореться з точністю машини, а в повітрі витає дух експерименту. Озирнись навколо.",
        "hint": "У цьому закладі перетинаються дві стихії: живий інтелект і холодний розрахунок. Тут немає битви, а скоріше танок, де кожен крок — виклик алгоритму, а кожен жест — натхнення творця. Назва нагадує про протистояння, що триває не тільки в каві, а й у світі ідей.",
        "answer": ["man versus machine"]
    },
    {
        "title": "Точка 8 — Місце формування генія",
        "text": "«Початок шляху — у стінах, де відлунюють думки юності.»",
        "question": "Підійди до Müllerstraße 11. Як називався заклад в цьому будинку, де молодий Ейнштейн розпочинав свій  шлях до великих відкриттів?",
        "hint": "Old tip l u. «Ім’я приховане в хаосі букв. Старе, шляхетне і має відгомін монархії...»",
        "answer": ["Luitpold Gymnasium"] 
    },
    {
        "title": "Точка 9 — Місце рівноваги",
        "text": "«Простір, де хаос і симетрія уклали давній пакт.»",
        "question": "Тут Ейнштейн міг би відчути логіку в лініях і гармонію в шумі. Відгадай назву цього живого механізму, що пульсує серцем міста вже століття.",
        "hint": "Пройди 550 м в напрямку північного сходу.",
        "answer": ["viktualienmarkt"]
    }
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
        message = f"{point['title']}\n\n{point['text']}\n\nЗавдання: {point['question']}\n\n📌 _Підказка:_ {point['hint']}"
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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    step = user_progress.get(user_id, 0)
    if step < len(QUEST):
        point = QUEST[step]
        user_answer = normalize_text(update.message.text)
        correct_answers = [normalize_text(ans) for ans in point["answer"]]
        if user_answer in correct_answers:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Вірно!")
            user_progress[user_id] = step + 1
            save_progress(user_progress)
            await send_quest_point(update, context)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Невірно. Спробуй ще раз.")

if __name__ == '__main__':
    application = ApplicationBuilder().token("7222439087:AAF4nAy9vsmr9TkIsVqojFnk8oevXJSKL-s").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    application.run_polling()

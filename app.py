import random
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Токен бота (читається з змінної середовища або заданий за замовчуванням)
TOKEN = os.environ.get("TOKEN", "7667222068:AAHIp4IJn9GXDkSrgy8D3XiRqxfG3K-fuGQ")

# Твій Telegram ID
ADMIN_ID = 529855903

# Список варіантів відповідей
REPLY_VARIANTS = [
    "Дякую за *питання*! Я відправив його команді. *Stay tuned*! 🚀\n\n📝 Ти можеш написати наступне питання прямо тут у чаті! 😊",
    "Ого, цікаве *питання*! Команда вже отримала його. Чекай відповіді! 😎\n\n📝 Ти можеш написати наступне питання прямо тут у чаті! 😊",
    "Класне *питання*! Я передав його *EnglishNerd*. Скоро буде відповідь! 💡\n\n📝 Ти можеш написати наступне питання прямо тут у чаті! 😊",
    "Супер, твоє *питання* у команді! *Keep asking*, і ми допоможемо! ✨\n\n📝 Ти можеш написати наступне питання прямо тут у чаті! 😊",
    "Чудове *питання*! Воно вже в команді. Буду тримати в курсі! 🌟\n\n📝 Ти можеш написати наступне питання прямо тут у чаті! 😊",
    "Твоє *питання* вражає! Передав команді, чекай новин! 🎉\n\n📝 Ти можеш написати наступне питання прямо тут у чаті! 😊",
    "Круто, що питаєш! *Питання* відправлено, відповідь буде скоро! 🔥\n\n📝 Ти можеш написати наступне питання прямо тут у чаті! 😊"
]

# Функція для створення інлайн-кнопки "Хочу стати студентом 🎓"
def create_register_button():
    keyboard = [
        [
            InlineKeyboardButton("🎓 Хочу стати студентом!", callback_data="register_for_lessons")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# Функція для створення інлайн-кнопки "Повернутися до питань 📝"
def create_return_button():
    keyboard = [
        [
            InlineKeyboardButton("📝 Повернутися до питань", callback_data="return_to_questions")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# Функція для створення інлайн-кнопки "Відмінити 📝"
def create_cancel_button():
    keyboard = [
        [
            InlineKeyboardButton("📝 Відмінити", callback_data="cancel_registration")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# Статус користувача
user_states = {}

# Команда /start (оновлена з гіперпосиланням і без прев’ю)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    # Скидаємо статус користувача при старті
    if user_id in user_states and user_states[user_id] == "locked":
        del user_states[user_id]
    await update.message.reply_text(
        "👋 Привіт! Я — *NerdHelperBot*. Допомагаю вивчати англійську разом! 😊\n\n"
        "📌 Ми обираємо *найцікавіші* питання і відповідаємо на них у каналі [EnglishNerd](https://t.me/englishnerd) — підпишись, щоб дізнаватися більше! "
        "На всі питання відповідаємо не одразу, але ми стараємося! 💡\n\n"
        "📝 Ти можеш надсилати *текст*, *фото* чи *відео* з питаннями. Натисни кнопку нижче!",
        parse_mode="Markdown",
        disable_web_page_preview=True,  # Прибираємо прев’ю посилання
        reply_markup=create_register_button()
    )
    await update.message.reply_text(
        "*Я чекаю на твоє запитання😊 👇*",
        parse_mode="Markdown"
    )

# Обробка натискання на інлайн-кнопки
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    callback_data = query.data

    if callback_data == "register_for_lessons":
        user_states[user_id] = "registration"
        await query.message.reply_text(
            "🎓 Класно! Давай запишемо тебе як студента! 😊\n"
            "Будь ласка, надішли всю інформацію одним повідомленням:\n\n"
            "📌 Як тебе звати?\n"
            "📌 Який у тебе рівень англійської (початковий, середній, просунутий)?\n"
            "📌 Як із тобою зв’язатися (наприклад, телефон чи Telegram)?",
            parse_mode="Markdown",
            reply_markup=create_cancel_button()
        )
    elif callback_data == "return_to_questions":
        if user_id in user_states and user_states[user_id] == "locked":
            del user_states[user_id]
            await query.message.reply_text(
                "✅ Ти повернувся! Задавай своє питання (текст, фото чи відео). Я передам його команді! 😊\n\n"
                "📝 Ти можеш написати наступне питання прямо тут у чаті!",
                parse_mode="Markdown"
            )
    elif callback_data == "cancel_registration":
        if user_id in user_states and user_states[user_id] == "registration":
            del user_states[user_id]
            await query.message.reply_text(
                "❌ Ти відмінив запис! Задавай своє питання (текст, фото чи відео). Я передам його команді! 😊\n\n"
                "📝 Ти можеш написати наступне питання прямо тут у чаті!",
                parse_mode="Markdown"
            )

# Обробка текстових повідомлень (питань)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user = update.message.from_user
    message_text = update.message.text

    # Якщо користувач заблокований (після опитувальника)
    if user_id in user_states and user_states[user_id] == "locked":
        await update.message.reply_text(
            "⛔ Ти тимчасово заблокований. Натисни 'Повернутися до питань', щоб продовжити! 😊",
            parse_mode="Markdown"
        )
        return

    # Якщо користувач у режимі опитування
    if user_id in user_states and user_states[user_id] == "registration":
        user_info = (
            f"🎓 Новий студент від @{user.username}:\n"
            f"Відповідь: {message_text}"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=user_info)
        await update.message.reply_text(
            "✅ Дякую за відповідь! Я передав твої дані команді. Очікуй зв’язку! 🎉",
            parse_mode="Markdown",
            reply_markup=create_return_button()
        )
        user_states[user_id] = "locked"
        return

    # Обробка звичайного текстового питання
    question = message_text
    user_info = f"📝 Користувач @{user.username} (ID: {user_id}) питає:\n{question}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=user_info)
    reply = random.choice(REPLY_VARIANTS)
    await update.message.reply_text(reply, parse_mode="Markdown")

# Обробка фотографій
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user = update.message.from_user
    photo = update.message.photo[-1]

    # Якщо користувач заблокований
    if user_id in user_states and user_states[user_id] == "locked":
        await update.message.reply_text(
            "⛔ Ти тимчасово заблокований. Натисни 'Повернутися до питань', щоб продовжити! 😊",
            parse_mode="Markdown"
        )
        return

    user_info = f"📸 Користувач @{user.username} (ID: {user_id}) надіслав фото:"
    await context.bot.send_message(chat_id=ADMIN_ID, text=user_info)
    await context.bot.send_photo(chat_id=ADMIN_ID, photo=photo.file_id)
    reply = random.choice(REPLY_VARIANTS)
    await update.message.reply_text(reply, parse_mode="Markdown")

# Обробка відео
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user = update.message.from_user
    video = update.message.video

    # Якщо користувач заблокований
    if user_id in user_states and user_states[user_id] == "locked":
        await update.message.reply_text(
            "⛔ Ти тимчасово заблокований. Натисни 'Повернутися до питань', щоб продовжити! 😊",
            parse_mode="Markdown"
        )
        return

    user_info = f"🎥 Користувач @{user.username} (ID: {user_id}) надіслав відео:"
    await context.bot.send_message(chat_id=ADMIN_ID, text=user_info)
    await context.bot.send_video(chat_id=ADMIN_ID, video=video.file_id)
    reply = random.choice(REPLY_VARIANTS)
    await update.message.reply_text(reply, parse_mode="Markdown")

# Головна функція для запуску бота
def main():
    app = Application.builder().token(TOKEN).build()

    # Додаємо обробники команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))

    # Запускаємо бота
    print("Бот запущений...")
    app.run_polling()

if __name__ == "__main__":
    main()

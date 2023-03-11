import sqlite3

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters

RECORD_PHONE, RECORD_NAME, RECORD_SURNAME, RECORD_CONFIRM = range(4)


# функция, вызываемая при старте бота
def start(update, context):
    user = update.message.from_user
    # Текст приветствия
    message = f"Привет, {user.first_name}! Я бот-ассистент. Чем я могу тебе помочь?"
    # Клавиатура
    keyboard = [
        [KeyboardButton("Запись на процедуру", callback_data='record')],
        [KeyboardButton("Про Девишник", callback_data='about')],
        [KeyboardButton("Виды процедур", callback_data='procedures')],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(message, reply_markup=reply_markup)


# Здесь будут различные процедуры, их описание и цены, мб картинки
def procedures(update, context):
    buttons = [
        InlineKeyboardButton(text="Массаж", callback_data="Massaj"),
        InlineKeyboardButton(text="Ноготочки", callback_data="Nogotochki"),
        InlineKeyboardButton(text="Дипиляция", callback_data="Dipilya"),
        InlineKeyboardButton(text="Парилка", callback_data="Parilka")
    ]
    # создаем разметку для клавиатуры
    keyboard = InlineKeyboardMarkup([buttons])
    # отправляем сообщение с клавиатурой
    context.bot.send_message(chat_id=update.effective_chat.id, text="Выберете, что вас интересует:",
                             reply_markup=keyboard)


# функция, вызываемая при нажатии на Про Девишник
def about(update, context):
    message = "Это прекрасное место в котором вы сможете почувствовать себя прекрасно, а так же набраться сил на ближайшую неделю)))."
    buttons = [["Запись на процедуру"], ["Про Девишник"], ["Связаться с нами"]]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(message, reply_markup=reply_markup)


def record(update, context):
    context.user_data["record"] = {}
    context.bot.send_message(chat_id=update.message.chat_id, text="Введите номер телефона:")
    return RECORD_PHONE

def record_phone(update, context):
    record = context.user_data["record"]
    record["phone"] = update.message.text
    context.bot.send_message(chat_id=update.message.chat_id, text="Введите фамилию:")
    return RECORD_NAME

def record_name(update, context):
    record = context.user_data["record"]
    record["name"] = update.message.text
    context.bot.send_message(chat_id=update.message.chat_id, text="Введите имя:")
    return RECORD_CONFIRM



# функция, вызываемая после ввода фамилии
def record_surname(update, context):
    user_data = context.user_data
    user_data["surname"] = update.message.text
    message = f"Спасибо за заполнение формы! Твои данные: {user_data}."
    update.message.reply_text(message)

    # Сохраняем данные пользователя в базу данных
    save_user_data(user_data["phone"], user_data["name"], user_data["surname"])

    # Отправляем сообщение о новой записи пользователю с ID @Goga111126
    context.bot.send_message(chat_id="@Goga111126", text=f"Добавлен пользователь {user_data['surname']}")

    return ConversationHandler.END


# функция, вызываемая при команде /cancel
def cancel(update, context):
    message = "Действие отменено. Введите /start для начала работы с ботом."
    update.message.reply_text(message)

    return ConversationHandler.END


# создаем Updater и Dispatcher
updater = Updater("5818832520:AAGvshlhmOZjtAVDRzV6c0RvEJsTMe-nqjQ")
dispatcher = updater.dispatcher


# создаем ConversationHandler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        RECORD_PHONE: [MessageHandler(Filters.text & ~Filters.command, record_name)],
        RECORD_NAME: [MessageHandler(Filters.text & ~Filters.command, record_surname)],
        RECORD_CONFIRM: [MessageHandler(Filters.text & ~Filters.command, record_confirm)],
    },
    fallbacks=[],
    allow_reentry=True
)
dispatcher.add_handler(conv_handler) # добавляем обработчик формы


# Добавляем обработчики команд
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text(r"Запись на процедуру"), record_phone))
dispatcher.add_handler(MessageHandler(Filters.text(r"Про Девишник"), about))
dispatcher.add_handler(MessageHandler(Filters.text(r"Виды процедур"), procedures))

# Запускаем цикл приема и обработки сообщений
updater.start_polling()
print('Bot started!!')
updater.idle()

# Сохранение в базу данных
def save_user_data(phone, first_name, last_name):
    conn = sqlite3.connect("static/users.db")
    cursor = conn.cursor()

    # Создаем таблицу, если ее еще нет
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        phone TEXT,
                        first_name TEXT,
                        last_name TEXT
                    )""")

    # Добавляем пользователя в базу данных
    cursor.execute("INSERT INTO users (phone, first_name, last_name) VALUES (?, ?, ?)", (phone, first_name, last_name))
    conn.commit()

    # Закрываем соединение с базой данных
    conn.close()

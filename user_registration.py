import Save_user_data

from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

# Определение состояний конверсации
PHONE, FIRST_NAME, LAST_NAME = range(3)

# Функция, запрашивающая номер телефона пользователя
def start(update, context):
    reply_keyboard = [['Cancel']]
    update.message.reply_text(
        'Введите ваш номер телефона в формате +79991234567',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return PHONE

# Функция, сохраняющая номер телефона и запрашивающая имя пользователя
def get_phone(update, context):
    user_phone = update.message.text
    # Здесь можно добавить код для проверки корректности номера телефона

    context.user_data['phone'] = user_phone

    reply_keyboard = [['Cancel']]
    update.message.reply_text(
        'Введите ваше имя',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return FIRST_NAME

# Функция, сохраняющая имя пользователя и запрашивающая фамилию пользователя
def get_first_name(update, context):
    user_first_name = update.message.text

    context.user_data['first_name'] = user_first_name

    reply_keyboard = [['Cancel']]
    update.message.reply_text(
        'Введите вашу фамилию',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return LAST_NAME

# Функция, сохраняющая фамилию пользователя и завершающая конверсацию
def get_last_name(update, context):
    user_last_name = update.message.text

    context.user_data['last_name'] = user_last_name

    # Здесь можно добавить код для сохранения данных пользователя в базе данных

    update.message.reply_text('Спасибо за регистрацию!')

    return ConversationHandler.END

# Функция, отменяющая регистрацию
def cancel(update, context):
    update.message.reply_text('Регистрация отменена.')
    return ConversationHandler.END

# Создание ConversationHandler
registration_handler = ConversationHandler(
    entry_points=[CommandHandler('register', start)],
    states={
        PHONE: [MessageHandler(Filters.regex('^\+7[0-9]{10}$'), get_phone)],
        FIRST_NAME: [MessageHandler(Filters.text & ~Filters.command, get_first_name)],
        LAST_NAME: [MessageHandler(Filters.text & ~Filters.command, get_last_name)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

Save_user_data.save_user_data(PHONE, FIRST_NAME, LAST_NAME)
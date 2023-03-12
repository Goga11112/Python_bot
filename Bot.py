import sqlite3
import config
import telegram
import user_registration

from About import about
from procedures import procedures
from Save_user_data import save_user_data
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters

# создаем Updater и Dispatcher
updater = Updater("5818832520:AAGvshlhmOZjtAVDRzV6c0RvEJsTMe-nqjQ")
dispatcher = updater.dispatcher


# функция, вызываемая при старте бота
def start(update, context):
    user = update.message.from_user
    # Текст приветствия
    message = f"Привет, {user.first_name}! Я бот-ассистент. Чем я могу тебе помочь?"
    telegram.Bot.send_sticker(user, config.sti)

    # Клавиатура
    keyboard = [
        [KeyboardButton("Запись на процедуру", callback_data='record')],
        [KeyboardButton("Про Девишник", callback_data='about')],
        [KeyboardButton("Виды процедур", callback_data='procedures')],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(message, reply_markup=reply_markup)


# Добавляем обработчики команд
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text(r"Запись на процедуру"), user_registration.start()))
dispatcher.add_handler(MessageHandler(Filters.text(r"Про Девишник"), about))
dispatcher.add_handler(MessageHandler(Filters.text(r"Виды процедур"), procedures))


# Запускаем цикл приема и обработки сообщений
updater.start_polling()
print('Bot started!!')
updater.idle()

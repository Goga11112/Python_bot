import Func_DB

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler

import main
from Func_DB import get_user
from main import dispatcher


def edit_user_data(update: Update, context: CallbackContext):
    # получаем id пользователя
    user_id = update.message.chat_id
    # ищем пользователя в базе данных
    user = get_user(user_id)
    # если пользователь найден
    if user:
        # получаем данные пользователя
        first_name = user[2]
        last_name = user[3]
        phone = user[4]
        # создаем клавиатуру для выбора, что редактировать
        keyboard = [[InlineKeyboardButton("Имя", callback_data='edit_first_name')],
                    [InlineKeyboardButton("Фамилия", callback_data='edit_last_name')],
                    [InlineKeyboardButton("Телефон", callback_data='edit_phone')],
                    [InlineKeyboardButton("Назад", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # отправляем пользователю клавиатуру
        context.bot.send_message(chat_id=user_id, text="Что вы хотите отредактировать?", reply_markup=reply_markup)

        # сохраняем данные пользователя в контексте для последующего использования
        context.user_data['user_id'] = user_id
        context.user_data['first_name'] = first_name
        context.user_data['last_name'] = last_name
        context.user_data['phone'] = phone

    # если пользователь не найден
    else:
        context.bot.send_message(chat_id=user_id, text="Вы не зарегистрированы. Введите /start для регистрации.")


dispatcher.add_handler(CallbackQueryHandler(Func_DB.edit_first_name, pattern='edit_first_name'))
dispatcher.add_handler(CallbackQueryHandler(Func_DB.edit_last_name, pattern='edit_last_name'))
dispatcher.add_handler(CallbackQueryHandler(Func_DB.edit_phone, pattern='edit_phone'))
dispatcher.add_handler(CallbackQueryHandler(main.main_menu, pattern='back'))
from telegram import Update
from telegram.ext import CallbackContext

from config import conn


def get_user(user_id):
    # Подключаемся к базе данных
    cursor = conn.cursor()

    # Выполняем запрос к базе данных
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()

    # Закрываем соединение с базой данных
    conn.close()

    # Если пользователь не найден, возвращаем None
    if not user:
        return None

    # Иначе возвращаем словарь с данными пользователя
    user_data = {
        'id': user[0],
        'first_name': user[1],
        'last_name': user[2],
        'phone': user[3]
    }
    return user_data


def update_user_data(user_id, first_name=None, last_name=None, phone=None):
    cursor = conn.cursor()

    if first_name:
        cursor.execute("UPDATE users SET first_name = ? WHERE id = ?", (first_name, user_id))
    if last_name:
        cursor.execute("UPDATE users SET last_name = ? WHERE id = ?", (last_name, user_id))
    if phone:
        cursor.execute("UPDATE users SET phone = ? WHERE id = ?", (phone, user_id))

    conn.commit()
    conn.close()


def edit_first_name(update: Update, context: CallbackContext):
    # получаем id пользователя из контекста
    user_id = context.user_data['user_id']
    # отправляем сообщение с просьбой ввести новое имя
    context.bot.send_message(chat_id=user_id, text="Введите новое имя:")
    # сохраняем выбранную опцию в контексте для последующего использования
    context.user_data['edit_option'] = 'edit_first_name'


def edit_last_name(update: Update, context: CallbackContext):
    # получаем id пользователя из контекста
    user_id = context.user_data['user_id']
    # отправляем сообщение с просьбой ввести новую фамилию
    context.bot.send_message(chat_id=user_id, text="Введите новую фамилию:")
    # сохраняем выбранную опцию в контексте для последующего использования
    context.user_data['edit_option'] = 'edit_last_name'


def edit_phone(update: Update, context: CallbackContext):
    # получаем id пользователя из контекста
    user_id = context.user_data['user_id']
    # отправляем сообщение с просьбой ввести новый номер телефона
    context.bot.send_message(chat_id=user_id, text="Введите новый номер телефона:")
    # сохраняем выбранную опцию в контексте для последующего использования
    context.user_data['edit_option'] = 'edit_phone'


def save_edited_data(update: Update, context: CallbackContext):
    # получаем id пользователя из контекста
    user_id = context.user_data['user_id']
    # получаем выбранную опцию из контекста
    edit_option = context.user_data['edit_option']
    # получаем данные, введенные пользователем
    edited_data = update.message.text
    # вызываем функцию обновления данных пользователя в базе данных
    if edit_option == 'edit_first_name':
        update_user_data(user_id, first_name=edited_data)
    elif edit_option == 'edit_last_name':
        update_user_data(user_id, last_name=edited_data)
    elif edit_option == 'edit_phone':
        update_user_data(user_id, phone=edited_data)
    # отправляем сообщение пользователю об успешном изменении данных
    context.bot.send_message(chat_id=user_id, text="Изменения успешно сохранены!")

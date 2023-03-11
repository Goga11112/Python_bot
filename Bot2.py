from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import random

# функция, вызываемая при старте бота
def start(update, context):
    user = update.message.from_user
    message = f"Привет, {user.first_name}! Я бот-ассистент. Чем я могу тебе помочь?"
    update.message.reply_text(message)

# функция, вызываемая при команде /help
def help_command(update, context):
    message = "Я могу генерировать случайные числа и сохранять твои данные в базу данных. " \
              "Для генерации случайного числа введи /random, " \
              "для сохранения своих данных введи /procedure."
    update.message.reply_text(message)

# функция, вызываемая при команде /random
def random_number(update, context):
    number = random.randint(1, 100)
    message = f"Случайное число: {number}"
    update.message.reply_text(message)

# функция, вызываемая при команде /procedure
def procedure(update, context):
    message = "Давай заполним форму. Введи свой номер телефона:"
    update.message.reply_text(message)
    return "phone"

# функция, вызываемая после ввода номера телефона
def phone(update, context):
    user_data = context.user_data
    user_data["phone"] = update.message.text
    message = "Теперь введи свое имя:"
    update.message.reply_text(message)
    return "name"

# функция, вызываемая после ввода имени
def name(update, context):
    user_data = context.user_data
    user_data["name"] = update.message.text
    message = "И фамилию:"
    update.message.reply_text(message)
    return "surname"

# функция, вызываемая после ввода фамилии
def surname(update, context):
    user_data = context.user_data
    user_data["surname"] = update.message.text
    message = f"Спасибо за заполнение формы! Твои данные: {user_data}."
    update.message.reply_text(message)

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
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('procedure', procedure)],
    states={
        "phone": [MessageHandler(Filters.text, phone)],
        "name": [MessageHandler(Filters.text, name)],
        "surname": [MessageHandler(Filters.text, surname)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
# добавляем обработчики команд
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("random", random_number))
dispatcher.add_handler(conversation_handler)
updater.start_polling()
updater.idle()
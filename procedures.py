from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# Здесь будут различные процедуры, их описание и цены, мб картинки
def procedures(update, context):
    buttons = [
        InlineKeyboardButton(text="Массаж", callback_data="Massaj"),
        InlineKeyboardButton(text="Ноготочки", callback_data="Nogotochki"),
        InlineKeyboardButton(text="Депиляция", callback_data="Dipilya"),
        InlineKeyboardButton(text="Парилка", callback_data="Parilka")
    ]
    # создаем разметку для клавиатуры
    keyboard = InlineKeyboardMarkup([buttons])
    # отправляем сообщение с клавиатурой
    context.bot.send_message(chat_id=update.effective_chat.id, text="Выберете, что вас интересует:",
                             reply_markup=keyboard)

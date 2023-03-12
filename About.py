from telegram import ReplyKeyboardMarkup


# функция, вызываемая при нажатии на Про Девишник
def about(update, context):
    message = "Это прекрасное место в котором вы сможете почувствовать себя прекрасно, а так же набраться сил на ближайшую неделю)))."
    buttons = [["Запись на процедуру"], ["Про Девишник"], ["Связаться с нами"]]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(message, reply_markup=reply_markup)
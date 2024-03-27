from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Получить информацию по товару 📑'
            ),
        ],
    ],
    resize_keyboard=True

)

reply_cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Отмена ❌'
            ),
        ],
    ],
    resize_keyboard=True
)

reply_keyboard_remove = ReplyKeyboardRemove()
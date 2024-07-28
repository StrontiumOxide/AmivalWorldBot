from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

remove = ReplyKeyboardRemove()

yes_no_caption_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Да ✅'),
            KeyboardButton(text='Нет ❌'),
        ]
    ], 
    resize_keyboard=True
)

anonymously_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Анонимно 😈'),
            KeyboardButton(text='Не анонимно 🌟'),
        ]
    ], 
    resize_keyboard=True
)

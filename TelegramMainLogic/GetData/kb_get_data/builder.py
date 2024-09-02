from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def created_username_kb(username: str) -> ReplyKeyboardMarkup:

    """
    Функция по созданию клавиатуры с ником пользователя
    """
    
    kb = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=f"@{username}")
        ]
    ],
    resize_keyboard=True)

    return kb

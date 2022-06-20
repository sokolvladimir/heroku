from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup
import emoji

start_idea = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🧠Начать!🧠", callback_data="start_idea"),
    ]
])

coin_idea = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="💸Да💸", callback_data="Yes"),
        InlineKeyboardButton(text="⛔Нет⛔", callback_data="No")
    ],
    [
        InlineKeyboardButton(text="🙄Возможно🙄", callback_data="maybe")
    ],
    [
        InlineKeyboardButton(text="😎Не важно😎", callback_data="Does_not_matter"),
        InlineKeyboardButton(text="😨Не знаю😨", callback_data="Do_not_know")
    ]
])
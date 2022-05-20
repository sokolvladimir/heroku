from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton("1")
b2 = KeyboardButton("2")
b3 = KeyboardButton("3")
b4 = KeyboardButton("4")
b5 = KeyboardButton("5")
b6 = KeyboardButton("6")
b7 = KeyboardButton("7")
del_button = KeyboardButton("/DELETE")

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
answer1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
answer_speciality = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
del_keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b1)
answer1.insert(b1).insert(b2).insert(b3).insert(b4)
answer_speciality.insert(b1).insert(b2).insert(b3).insert(b4).insert(b5).insert(b6)
del_keyb.add(del_button)
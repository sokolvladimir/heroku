from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup
import emoji


social_media = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton("Instagram", url="https://www.instagram.com/"),
        InlineKeyboardButton("Linkedin", url="https://www.linkedin.com/")
    ]
])

answer_yes_no = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="ДА" + emoji.emojize(":check_mark:"), callback_data="YES"),
        InlineKeyboardButton(text="НЕТ" + emoji.emojize(":cross_mark:"), callback_data="NO"),
    ]
])
# Кнопка вабора специальности
kb_speciality = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(text=emoji.emojize(':cowboy_hat_face:') + "Бэкэнд", callback_data="speciality_backend"),
        InlineKeyboardButton(text=emoji.emojize(':smiling_face_with_sunglasses:') + "Фронтэнд",
                             callback_data="speciality_frontend")

    ],
    [
        InlineKeyboardButton(text=emoji.emojize(':artist:') + "Дизайн", callback_data="speciality_design"),
        InlineKeyboardButton(text=emoji.emojize(':exploding_head:') + "Тестировка", callback_data="speciality_testing")
    ],
    [
        InlineKeyboardButton(text=emoji.emojize(':man_technologist:') + "Мобильная разработка",
                         callback_data="speciality_mobile_dev"),
        InlineKeyboardButton(text=emoji.emojize(':detective:') + "Рекрутер", callback_data="speciality_recruiter")

    ],
    [
        InlineKeyboardButton(text=emoji.emojize(':face_with_rolling_eyes:') + "Другое", callback_data="speciality_etc")
    ]
])

# Как вы о нас узнали
source_exlab = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(text="LinkedIn", callback_data="source_linkedin"),
        InlineKeyboardButton(text="Instagram", callback_data="source_instagram")
    ],
    [
        InlineKeyboardButton(text="Facebook", callback_data="source_facebook"),
        InlineKeyboardButton(text="Google", callback_data="source_google")
    ],
    [
        InlineKeyboardButton(text="Другие социальные сети", callback_data="source_etc"),
        InlineKeyboardButton(text="От друзей", callback_data="source_friends")
    ]
])

# Уровень владения Английским
english_level = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="A1", callback_data="en_level_A1"),
        InlineKeyboardButton(text="A2", callback_data="en_level_A2")
    ],
    [
        InlineKeyboardButton(text="B1", callback_data="en_level_B1"),
        InlineKeyboardButton(text="B2", callback_data="en_level_B2")
    ],
    [
        InlineKeyboardButton(text="C1", callback_data="en_level_C1"),
        InlineKeyboardButton(text="C2", callback_data="en_level_C2")
    ]
])

# Кнопка старта опроса
start_kb_first = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Пройти тест " + emoji.emojize(':thinking_face:'),
                             callback_data="start_quiz")
    ]
])

del_unsub = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=emoji.emojize(":skull_and_crossbones:") + "Удалить", callback_data="delete"),
        InlineKeyboardButton(text=emoji.emojize(":smiling_face_with_horns:") + "Отписаться",
                             callback_data="unsubscribe")
    ]
])

del_sub = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=emoji.emojize(":skull_and_crossbones:") + "Удалить", callback_data="delete"),
        InlineKeyboardButton(text=emoji.emojize(":smiling_face_with_halo:") + "Подписаться", callback_data="subscribe")
    ]
])

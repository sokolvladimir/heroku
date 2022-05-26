from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup
import emoji


social_media = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton("Instagram", url="https://instagram.com/exlab_startup?igshid=YmMyMTA2M2Y="),
        InlineKeyboardButton("Linkedin", url="https://www.linkedin.com/company/exlab-start-up/"),
    ],
    [
        InlineKeyboardButton("Telegram", url="https://t.me/ExLabChannel"),
        InlineKeyboardButton("YouTube", url="https://youtube.com/channel/UC-TAnVYVN7qg5dgsYQJkuvA")
    ]
])

join_group = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton("Вступить в ExLab group", url="https://t.me/ExperienceLaboratory")
    ]
])

rules = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton("Правила сообщества", url="https://docs.google.com/document/d/1uC"
                                                              "xWJUxWfDX0yK2_WGil0K-w5N5HK3HTxlxXvLlbNrI/edit")
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
        InlineKeyboardButton(text=emoji.emojize(':cowboy_hat_face:') + "Backend", callback_data="speciality_backend"),
        InlineKeyboardButton(text=emoji.emojize(':smiling_face_with_sunglasses:') + "Frontend",
                             callback_data="speciality_frontend")

    ],
    [
        InlineKeyboardButton(text=emoji.emojize(':artist:') + "Design", callback_data="speciality_design"),
        InlineKeyboardButton(text=emoji.emojize(':man_technologist:') + "Mobile development",
                             callback_data="speciality_mobile_dev")
    ],
    [
        InlineKeyboardButton(text=emoji.emojize(':detective:') + "Recruiter, HR", callback_data="speciality_recruiter"),
        InlineKeyboardButton(text=emoji.emojize(':person_facepalming:') + "QA",
                             callback_data="speciality_QA")
    ],
    [
        InlineKeyboardButton(text=emoji.emojize(':person_shrugging:') + "BA", callback_data="speciality_BA"),
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
        InlineKeyboardButton(text="По рекомендации", callback_data="source_friends"),
        InlineKeyboardButton(text="Telegram", callback_data="source_Telegram")
    ],
    [
        InlineKeyboardButton(text="Другое", callback_data="source_etc")
    ]
])

# Уровень владения Английским
english_level = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Beginner (A1)", callback_data="en_level_A1"),
        InlineKeyboardButton(text="Elementary (A2)", callback_data="en_level_A2")
    ],
    [
        InlineKeyboardButton(text="Intermediate (B1)", callback_data="en_level_B1"),
        InlineKeyboardButton(text="Upper Intermediate (B2)", callback_data="en_level_B2")
    ],
    [
        InlineKeyboardButton(text="Advanced (C1)", callback_data="en_level_C1"),
        InlineKeyboardButton(text="Proficiency (C2)", callback_data="en_level_C2")
    ]
])

# Кнопка старта опроса
start_kb_first = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Давай начнём!" + emoji.emojize(':thinking_face:'),
                             callback_data="start_quiz")
    ]
])

# del_unsub = InlineKeyboardMarkup(inline_keyboard=[
#     [
#         InlineKeyboardButton(text=emoji.emojize(":skull_and_crossbones:") + "Удалить", callback_data="delete"),
#         InlineKeyboardButton(text=emoji.emojize(":smiling_face_with_horns:") + "Отписаться",
#                              callback_data="unsubscribe")
#     ]
# ])
#
# del_sub = InlineKeyboardMarkup(inline_keyboard=[
#     [
#         InlineKeyboardButton(text=emoji.emojize(":skull_and_crossbones:") + "Удалить", callback_data="delete"),
#         InlineKeyboardButton(text=emoji.emojize(":smiling_face_with_halo:") + "Подписаться", callback_data="subscribe")
#     ]
# ])

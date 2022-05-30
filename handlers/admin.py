from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from aiogram import types, Dispatcher
from keyboards import *
from create_bot import db
import emoji
import datetime
import time
from aiogram.types import KeyboardButton, ReplyKeyboardRemove
import validators
import psycopg2
from psycopg2.errors import *

class FSMAdmin(StatesGroup):
    question_name = State()
    question_birth = State()
    question_city = State()
    question_speciality = State()
    question_spec_etc = State()
    question_specialization = State()
    question_course = State()
    question_eng = State()
    question_linkedin = State()
    question_portfolio = State()
    question_sours = State()
    question_sours_etc = State()
    question_reason = State()
    question_idea = State()


async def start_program(message: types.Message):
    if not db.user_exists(int(message.from_user.id)):
        #db.user_exists(int(message.from_user.id))
        print(db.user_exists(message.from_user.id))
        await message.answer(f"Привет! Я ExLab Registration Bot!\n" + emoji.emojize(":vulcan_salute:") +
                             f"Я помогу тебе пройти опрос и стать частью команды ExLab!", reply_markup=start_kb_first)
    else:
        print(db.user_exists(int(message.from_user.id)))
        await message.answer("Привет!\nТы уже успешно прошел опрос.")


async def start_question(call: types.CallbackQuery):
    db.add_user(call.from_user.id, call.from_user.username)
    await FSMAdmin.question_name.set()
    await bot.send_message(call.from_user.id, "Как тебя зовут🖐️?\nВведи фамилию и имя.")


async def question_name(message: types.Message):
    db.set_username(message.from_user.id, message.text)
    await FSMAdmin.next()
    await message.answer(emoji.emojize(":baby:") + "Укажи дату рождения.\n(dd.mm.yyyy)")


async def birth_day(message: types.Message):
    try:
        date_correct_dbase_format = datetime.datetime.strptime(message.text, "%d.%m.%Y").strftime("%Y-%m-%d")
        db.birthday(message.from_user.id, date_correct_dbase_format)
        await FSMAdmin.next()
        await message.answer(emoji.emojize(":cityscape:") + "Откуда ты?\n"
                                                            "Укажи страну и город.")
    except ValueError:
        var = FSMAdmin.question_birth
        await bot.send_message(message.from_user.id, "Введите корректную дату в формате: день.месяц.год")


async def question_city(message: types.Message):
    db.set_city(message.from_user.id, message.text)
    await FSMAdmin.next()
    await message.answer(emoji.emojize(":mechanic:") + "Выбери свою специальнось.", reply_markup=kb_speciality)


async def my_speciality(message: types.Message):
    db.set_speciality(message.from_user.id, message.text)
    await FSMAdmin.next()
    await message.answer("Расскажи о своем обучении по этой специальности.")


async def question_speciality(call: types.CallbackQuery):
    if call.data == "speciality_etc":
        await bot.send_message(call.from_user.id, "Какая у тебя специальность?")
        await FSMAdmin.question_spec_etc.set()
    else:
        db.set_speciality(call.from_user.id, call.data)
        await FSMAdmin.question_specialization.set()
        await bot.send_message(call.from_user.id, "Расскажи о своем обучении по этой специальности.")


async def question_specialization(message: types.Message):
    db.set_specialization(message.from_user.id, message.text)
    await FSMAdmin.next()
    await message.answer(emoji.emojize(":graduation_cap:") + "Какой у тебя стек технологий?")


async def question_courses(message: types.Message):
    db.set_courses(message.from_user.id, message.text)
    await FSMAdmin.next()
    await message.answer(emoji.emojize(":face_with_tongue:") + "Уровень владения английским?",
                         reply_markup=english_level)


async def eng_lev(call: types.CallbackQuery):
    db.set_eng(call.from_user.id, call.data)
    await FSMAdmin.next()
    await bot.send_message(call.from_user.id, emoji.emojize(":link:") + "Обязательно добавь ссылку на свой Linkedin.\n"
                                                                        "Так рекрутер сможет быстрее с тобой связаться."
                                                                        "\nПример: https://www.linkedin.com/in/"
                                                                        "persone/")


async def link_linkedin(message: types.Message, state: FSMContext):
    txt = "https://www.linkedin.com/"
    if txt not in message.text:
        await message.answer(emoji.emojize(":face_screaming_in_fear:") + "Ты ввел некорректные данные! "
                            "Попробуйте еще раз!" + emoji.emojize(":face_screaming_in_fear:") +
                            "Пример: https://www.linkedin.com/in/persone/")
        await FSMAdmin.question_linkedin.set()
    else:
        db.set_links(message.from_user.id, message.text)
        await FSMAdmin.next()
        await message.answer("Прикрепи ссылку на свое портфолио. Если оно есть.",
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                             .insert(KeyboardButton("Пропустить")))


async def portfolio(message: types.Message):
    if message.text == "Пропустить":
        await FSMAdmin.next()
        await message.answer(emoji.emojize(":ear:") + "Как ты узнал об ExLab?\n", reply_markup=source_exlab)
    else:
        if validators.url(message.text) is True:
            db.set_portfolio(message.from_user.id, message.text)
            await FSMAdmin.next()
            await message.answer(emoji.emojize(":ear:") + "Как ты узнал об ExLab?\n", reply_markup=source_exlab)
        else:
            await message.answer("!Ты ввел некорректный URL!\nПопробуй еще раз.")
            await FSMAdmin.question_portfolio.set()


async def sourse_exlab_etc(message: types.Message):
    db.set_sourse(message.from_user.id, message.text)
    await FSMAdmin.next()
    await message.answer(emoji.emojize(":white_question_mark:") + "Почему ты решил присоединиться "
                                                            "к ExLab?" + emoji.emojize(":white_question_mark:"))


async def sourse_exlab(call: types.CallbackQuery):
    if call.data == "source_etc":
        await bot.send_message(call.from_user.id, "Как именно ты о нас узнал?", reply_markup=ReplyKeyboardRemove())
        await FSMAdmin.question_sours_etc.set()
    else:
        db.set_sourse(call.from_user.id, call.data)
        await FSMAdmin.question_reason.set()
        await bot.send_message(call.from_user.id, emoji.emojize(":white_question_mark:") +
                               "Почему ты решил присоединиться к ExLab?" + emoji.emojize(":white_question_mark:"),
                               reply_markup=ReplyKeyboardRemove())


async def reason_exlab(message: types.Message, state: FSMContext):
    db.set_reason(message.from_user.id, message.text)
    await FSMAdmin.next()
    await message.answer(emoji.emojize(":gem_stone:") + "У тебя есть идея, которую мы могли бы реализовать вместе?" +
                         emoji.emojize(":gem_stone:"), reply_markup=answer_yes_no)


async def idea_exlab(call: types.CallbackQuery, state: FSMContext):
    db.set_idea(call.from_user.id, call.data)
    await bot.send_message(call.from_user.id, text="Добро пожаловать в ExLab!\nВ нашей телеграмм-группе ты сможешь "
                                                   "познакомиться с другими участниками проекта.",
                           reply_markup=join_group)
    time.sleep(10)
    await bot.send_message(call.from_user.id, text="Ознакомься с правилами нашего сообщества.", reply_markup=rules)
    time.sleep(10)
    await bot.send_message(call.from_user.id, text="Подписывайся на наши соц сети, чтобы быть в курсе всех новостей "
                                                   "ExLab.", reply_markup=social_media)
    await bot.send_message(call.from_user.id, "Спасибо за регистрацию. Рады, что ты с нами!")
    await state.finish()


# async def unsubscribe(call: types.CallbackQuery):
#     if call.data == "unsubscribe":
#         db.set_signup(call.from_user.id, False)
#         await call.message.delete()
#         await bot.send_message(call.from_user.id, "Ты отписался от рассылки", reply_markup=del_sub)
#     else:
#         db.set_signup(call.from_user.id, True)
#         await call.message.delete()
#         await bot.send_message(call.from_user.id, "Ты подписался на рассылку", reply_markup=del_unsub)


async def del_user(call: types.CallbackQuery):
    db.user_del(call.from_user.id)
    await call.message.delete()
    await bot.send_message(call.from_user.id, emoji.emojize(":loudly_crying_face:") + "Ты успешно удалил пользователя!"
                           + emoji.emojize(":loudly_crying_face:"), reply_markup=start_kb_first)


def register_handlers_admin(dp: Dispatcher):

    dp.register_message_handler(start_program, commands="start")
    dp.register_callback_query_handler(start_question, text="start_quiz")
    dp.register_message_handler(question_name, content_types=["text"], state=FSMAdmin.question_name)
    dp.register_message_handler(birth_day, content_types=["text"], state=FSMAdmin.question_birth)
    dp.register_message_handler(question_city, content_types=["text"], state=FSMAdmin.question_city)
    dp.register_callback_query_handler(question_speciality, text_contains="speciality",
                                       state=FSMAdmin.question_speciality)
    dp.register_message_handler(my_speciality, content_types=["text"], state=FSMAdmin.question_spec_etc)
    dp.register_message_handler(question_specialization, content_types=["text"], state=FSMAdmin.question_specialization)
    dp.register_message_handler(question_courses, content_types=["text"], state=FSMAdmin.question_course)
    dp.register_callback_query_handler(eng_lev, text_contains="en_level", state=FSMAdmin.question_eng)
    dp.register_message_handler(link_linkedin, content_types=["text"], state=FSMAdmin.question_linkedin)
    dp.register_message_handler(portfolio, content_types=["text"], state=FSMAdmin.question_portfolio)
    dp.register_callback_query_handler(sourse_exlab, text_contains="source", state=FSMAdmin.question_sours)
    dp.register_message_handler(sourse_exlab_etc, content_types=["text"], state=FSMAdmin.question_sours_etc)
    dp.register_message_handler(reason_exlab, content_types=["text"], state=FSMAdmin.question_reason)
    dp.register_callback_query_handler(idea_exlab, text=["YES", "NO"], state=FSMAdmin.question_idea)
    dp.register_callback_query_handler(del_user, text="delete")
    # dp.register_callback_query_handler(unsubscribe, text_contains="subscribe")

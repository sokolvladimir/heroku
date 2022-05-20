from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from keyboards import *
from create_bot import db
import asyncio
import time


class FSMAdmin(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()
    question_8 = State()
    question_9 = State()

# @dp.message_handler(commands="Опрос", state=None)
async def start_question(message: types.Message):
    """Проверка прохождения теста пользователем"""
    if not db.user_exists(int(message.from_user.id)):
        db.add_user(message.from_user.id, message.from_user.username)
        await FSMAdmin.question_1.set()
        await message.answer("Как вас зовут?\nПример:\nФёдоров Алексей")
    else:
        await message.answer("Вы уже успешно прошли регистрацию!")
        await db.read_user(message.from_user.id, message)


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_1)
async def question_name(message: types.Message):
    db.set_username(message.from_user.id, message.text)
    await FSMAdmin.next()
    await message.answer("Из какого вы города?")


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_2)
async def question_city(message: types.Message):
    if message.text != "Минск":
        await message.answer("Введите Минск")
        var = FSMAdmin.question_2
    else:
        db.set_city(message.from_user.id, message.text)
        await FSMAdmin.next()
        await message.answer("Какая у вас специальность?\n"
                             "1. Бэкэнд\n"
                             "2. Фронтэнд\n"
                             "3. Дизайн\n"
                             "4. Тестировка\n"
                             "5. Мобильная разработка\n"
                             "6. Рекрутер\n"
                             "Если другое напишите сообщением!", reply_markup=answer_speciality_eng)


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_3)
async def question_speciality(message: types.Message, state: FSMContext):
    db.set_speciality(message.from_user.id, message.text)
    await FSMAdmin.next()
    await message.answer("Как получал знания, какие курсы заканчивал?")


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_4)
async def question_courses(message: types.Message, state: FSMContext):
    db.set_courses(message.from_user.id, message.text)
    await FSMAdmin.next()
    await message.answer("Какой у Вас уровень владения английским языком?\n"
                         "1: A1\n"
                         "2: A2\n"
                         "3: B1\n"
                         "4: B2\n"
                         "5: C1\n"
                         "6: C2", reply_markup=answer_speciality_eng)
#    await state.finish()


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_5)
async def eng_lev(message: types.Message, state: FSMContext):
    lst_ = ["1", "A1", "2", "A2", "3", "B1", "4", "B2",
            "5", "C1", "6", "C2"]
    if message.text not in lst_:
        await message.answer("Вы ввели некорректные данные! Попробуйте ещё!")
        print(type(message.text))
        var = FSMAdmin.question_5
    else:
        db.set_eng(message.from_user.id, message.text)
        await FSMAdmin.next()
        await message.answer("Добавьте ссылку на ваш LinkedIn\n"
                             "Пример: https://www.linkedin.com/in/persone/", reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_6)
async def link_linkedin(message: types.Message, state: FSMContext):
    txt = "https://www.linkedin.com/"
    if txt not in message.text:
        await message.answer("Вы ввели некорректные данные! Попробуйте ещё!\n"
                             "Пример: https://www.linkedin.com/in/persone/")
        var = FSMAdmin.question_6
    else:
        db.set_links(message.from_user.id, message.text)
        await FSMAdmin.next()
        await message.answer("Как ты узнал о ExLab?\n"
                             "1: LinkedIn\n"
                             "2: Instagram\n"
                             "3: Facebook\n"
                             "4: Google\n"
                             "5: Другие социальные сети\n"
                             "6: От друзей (по рекомендации)\n"
                             "Если другое напишите сообщением!", reply_markup=answer_speciality_eng)


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_7)
async def sourse_exlab(message: types.Message, state: FSMContext):
    db.set_sourse(message.from_user.id, message.text)
    await FSMAdmin.next()
    await message.answer("Почему ты решил присоедениться к ExLab?", reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_8)
async def reason_exlab(message: types.Message, state: FSMContext):
    db.set_reason(message.from_user.id, message.text)
    await FSMAdmin.next()
    await message.answer("Есть ли у тебя идея, которую мы могли бы "
                         "совместно реализовать?", reply_markup=answer_yes_no)


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_9)
async def idea_exlab(message: types.Message, state: FSMContext):
    db.set_idea(message.from_user.id, message.text)
    await message.answer("Спасибо за регистрацию - подписывайтесь на канал, "
                         "ставьте лайки, не забывайте нажать на колокольчик "
                         "что-бы не пропускать уведомления! "
                         "Вот ссылки на наши соц сети", reply_markup=social_media)
    await state.finish()


async def del_user(message: types.Message):
    db.user_del(message.from_user.id)
    await message.answer("Вы успешно удалили пользователя!")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(start_question, commands="Опрос", state=None)
    dp.register_message_handler(question_name, content_types=["text"], state=FSMAdmin.question_1)
    dp.register_message_handler(question_city, content_types=["text"], state=FSMAdmin.question_2)
    dp.register_message_handler(question_speciality, content_types=["text"], state=FSMAdmin.question_3)
    dp.register_message_handler(question_courses, content_types=["text"], state=FSMAdmin.question_4)
    dp.register_message_handler(eng_lev, content_types=["text"], state=FSMAdmin.question_5)
    dp.register_message_handler(link_linkedin, content_types=["text"], state=FSMAdmin.question_6)
    dp.register_message_handler(sourse_exlab, content_types=["text"], state=FSMAdmin.question_7)
    dp.register_message_handler(reason_exlab, content_types=["text"], state=FSMAdmin.question_8)
    dp.register_message_handler(idea_exlab, content_types=["text"], state=FSMAdmin.question_9)
    dp.register_message_handler(del_user, commands="DELETE")

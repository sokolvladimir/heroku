from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from keyboards import kb_client, answer1, answer_speciality, del_keyb
from create_bot import db
import asyncio
import time


class FSMAdmin(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()


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
        FSMAdmin.question_2
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
                             "Если другое напишите сообщением!", reply_markup=answer_speciality)


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_3)
async def question_speciality(message: types.Message, state: FSMContext):
    db.set_speciality(message.from_user.id, message.text)
    await FSMAdmin.next()
    await message.answer("Как получал знания, какие курсы заканчивал?")


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_4)
async def question_courses(message: types.Message, state: FSMContext):
    db.set_courses(message.from_user.id, message.text)
    await message.answer("Вы успешно прошли регистрацию!", reply_markup=ReplyKeyboardRemove())
    await db.read_user(message.from_user.id, message)
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
    dp.register_message_handler(del_user, commands="DELETE")

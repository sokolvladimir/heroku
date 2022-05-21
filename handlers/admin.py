from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from keyboards import *
from create_bot import db
import asyncio
import time
import emoji


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


# @dp.message_handler(commands="start")
async def start_program(message: types.Message):
    if not db.user_exists(int(message.from_user.id)):
        await message.answer(f"Привет {message.from_user.username}!\n"
                             f"Вы можете пройти опрос и стать участником "
                             f"команды ExLab", reply_markup=start_kb_first)
    else:
        await message.answer(f"Привет {db.name_user(message.from_user.id)}!\n"
                             f"Вы уже успешно прошли опрос, если вас не устраивают "
                             f"принципы нашего сообщества или не хотите получать рассылку"
                             f"нажмите на соответствующую кнопку=)", reply_markup=del_unsub)


# @dp.callback_query_handler(text="start_quiz")
async def start_question(call: types.CallbackQuery):
    db.add_user(call.from_user.id, call.from_user.username)
    await FSMAdmin.question_1.set()
    await bot.send_message(call.from_user.id, "Как вас зовут?" + emoji.emojize(":waving_hand:") +
                           "\nПример:\nФёдоров Алексей")

# @dp.callback_query_handler(text="start_quiz")
# async def start_question(message: types.Message):
#     """Проверка прохождения теста пользователем"""
#     if not db.user_exists(int(message.from_user.id)):
#         db.add_user(message.from_user.id, message.from_user.username)
#         await FSMAdmin.question_1.set()
#         await message.answer("Как вас зовут?\nПример:\nФёдоров Алексей")
#     else:
#         await message.answer("Вы уже успешно прошли регистрацию!")
#         await db.read_user(message.from_user.id, message)


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_1)
async def question_name(message: types.Message):
    db.set_username(message.from_user.id, message.text)
    await FSMAdmin.next()
    await message.answer(emoji.emojize(":cityscape:") + "Из какого вы города?")


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_2)
async def question_city(message: types.Message):
        db.set_city(message.from_user.id, message.text)
        await FSMAdmin.next()
        await message.answer(emoji.emojize(":mechanic:") + "Какая у вас специальность?", reply_markup=kb_speciality)


# @dp.callback_query_handler(text_contains="speciality", state=FSMAdmin.question_3)
async def question_speciality(call: types.CallbackQuery):
    #await bot.delete_message(call.from_user.id, call.message.message_id)
    db.set_speciality(call.from_user.id, call.data)
    await FSMAdmin.next()
    await bot.send_message(call.from_user.id, emoji.emojize(":graduation_cap:") + "Как получал знания, какие "
                                                                                  "курсы заканчивал?")

# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_3)
# async def question_speciality(message: types.Message, state: FSMContext):
#     db.set_speciality(message.from_user.id, message.text)
#     await FSMAdmin.next()
#     await message.answer("Как получал знания, какие курсы заканчивал?")


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_4)
async def question_courses(message: types.Message, state: FSMContext):
    db.set_courses(message.from_user.id, message.text)
    await FSMAdmin.next()
    await message.answer(emoji.emojize(":face_with_tongue:") + "Какой у Вас уровень владения английским языком?",
                         reply_markup=english_level)


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_5)
async def eng_lev(call: types.CallbackQuery):
    db.set_eng(call.from_user.id, call.data)
    await FSMAdmin.next()
    await bot.send_message(call.from_user.id, emoji.emojize(":link:") + "Добавьте ссылку на ваш LinkedIn" +
                                                                        "\nПример: https://www.linkedin.com/in/"
                                                                        "persone/")


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_6)
async def link_linkedin(message: types.Message, state: FSMContext):
    txt = "https://www.linkedin.com/"
    if txt not in message.text:
        await message.answer(emoji.emojize(":face_screaming_in_fear:") + "Вы ввели некорректные данные! "
                            "Попробуйте ещё!" + emoji.emojize(":face_screaming_in_fear:") +
                            "Пример: https://www.linkedin.com/in/persone/")
        var = FSMAdmin.question_6
    else:
        db.set_links(message.from_user.id, message.text)
        await FSMAdmin.next()
        await message.answer(emoji.emojize(":ear:") + "Как ты узнал о ExLab?\n", reply_markup=source_exlab)


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_7)
async def sourse_exlab(call: types.CallbackQuery):
    db.set_sourse(call.from_user.id, call.data)
    await FSMAdmin.next()
    await bot.send_message(call.from_user.id, emoji.emojize(":white_question_mark:") + "Почему ты решил присоедениться "
                                                            "к ExLab?" + emoji.emojize(":white_question_mark:"))


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_8)
async def reason_exlab(message: types.Message, state: FSMContext):
    db.set_reason(message.from_user.id, message.text)
    await FSMAdmin.next()
    await message.answer(emoji.emojize(":gem_stone:") + "Есть ли у тебя идея, которую мы могли бы "
                         "совместно реализовать?" + emoji.emojize(":gem_stone:"), reply_markup=answer_yes_no)


# @dp.message_handler(content_types=["text"], state=FSMAdmin.question_9)
async def idea_exlab(call: types.CallbackQuery, state: FSMContext):
    db.set_idea(call.from_user.id, call.data)
    await bot.send_message(call.from_user.id, text="Подписывайтесь на канал, " + emoji.emojize(":writing_hand:") +
                         "ставьте лайки" + emoji.emojize(":thumbs_up:") + ", не забывайте нажать на колокольчик " +
                         emoji.emojize(":bell:") + "что-бы не пропускать уведомления! " + emoji.emojize(":loudspeaker:")
                         + "Вот ссылки на наши соц сети", reply_markup=social_media)
    await bot.send_message(call.from_user.id, "Спасибо за регистрацию!", reply_markup=del_unsub)
    await state.finish()


async def unsubscribe(call: types.CallbackQuery):
    if call.data == "unsubscribe":
        db.set_signup(call.from_user.id, 0)
        await call.message.delete()
        await bot.send_message(call.from_user.id, "Вы отписались от рассылки", reply_markup=del_sub)
    else:
        db.set_signup(call.from_user.id, 1)
        await call.message.delete()
        await bot.send_message(call.from_user.id, "Вы подписались на рассылку", reply_markup=del_unsub)



async def del_user(call: types.CallbackQuery):
    db.user_del(call.from_user.id)
    await call.message.delete()
    await bot.send_message(call.from_user.id,emoji.emojize(":loudly_crying_face:") + "Вы успешно удалили пользователя!"
                           + emoji.emojize(":loudly_crying_face:"), reply_markup=start_kb_first)


def register_handlers_admin(dp: Dispatcher):

    dp.register_message_handler(start_program, commands="start")
    dp.register_callback_query_handler(start_question, text="start_quiz")
    dp.register_message_handler(question_name, content_types=["text"], state=FSMAdmin.question_1)
    dp.register_message_handler(question_city, content_types=["text"], state=FSMAdmin.question_2)
    dp.register_callback_query_handler(question_speciality, text_contains="speciality", state=FSMAdmin.question_3)
    dp.register_message_handler(question_courses, content_types=["text"], state=FSMAdmin.question_4)
    dp.register_callback_query_handler(eng_lev, text_contains="en_level", state=FSMAdmin.question_5)
    dp.register_message_handler(link_linkedin, content_types=["text"], state=FSMAdmin.question_6)
    dp.register_callback_query_handler(sourse_exlab, text_contains="source", state=FSMAdmin.question_7)
    dp.register_message_handler(reason_exlab, content_types=["text"], state=FSMAdmin.question_8)
    dp.register_callback_query_handler(idea_exlab, text=["YES", "NO"], state=FSMAdmin.question_9)
    dp.register_callback_query_handler(del_user, text="delete")
    dp.register_callback_query_handler(unsubscribe, text_contains="subscribe")

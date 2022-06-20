from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import bot, db, Nastya_id
from keyboards import *


class FSMInterview(StatesGroup):
    about = State()
    problem = State()
    audience = State()
    how_work = State()
    differences = State()
    monetization = State()


# async def start_idea(call: types.CallbackQuery):
#     await FSMInterview.about.set()
#     await bot.send_message(call.from_user.id, "Кратко расскажи о своем проекте.")
async def start_idea(message: types.Message):
    await FSMInterview.about.set()
    await message.answer("Кратко расскажи о своем проекте.")


async def about_idea(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.from_user.id
        data['about'] = message.text
    await FSMInterview.next()
    await message.answer("Какую проблему поможет решить твой проект?")


async def problem_idea(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['problem'] = message.text
    await FSMInterview.next()
    await message.answer("Опиши примерную целевую аудиторию твоего проекта.")


async def audience_idea(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['audience'] = message.text
    await FSMInterview.next()
    await message.answer("Опиши подробнее, как будет работать проект.")


async def how_work_idea(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['how_work'] = message.text
    await FSMInterview.next()
    await message.answer("Есть ли какие-то особенности у твоего проекта? Чем он будет отличаться от других похожих "
                         "продуктов?")


async def differences_idea(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['differences'] = message.text
    await FSMInterview.next()
    await message.answer("Хотелось бы тебе монетизировать конечный результат?", reply_markup=coin_idea)


async def monetization_idea(call: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        data['monetization'] = call.data
    await FSMInterview.next()
    await bot.send_message(call.from_user.id, "Спасибо!\nА теперь менторы займутся анализом идей и с помощью "
                                              "голосования мы выберем несколько проектов для дальнейшей разработки. "
                                              "Возможно, это будет именно твой проект!\nМы обязательно дадим тебе "
                                              "обратную связь, независимо от результата.\nСледи за новостями на нашем "
                                              "Telegram-канале.\nКоманда ExLab.")
    async with state.proxy() as data:
        db.add_idea(data)
        await bot.send_message(Nastya_id, text=f"Анастасия холопы подкинули новую идею!!"
                                               f"\nО проекте:\n{data['about']}"
                                               f"\nКакую проблему решает проект:\n{data['problem']}"
                                               f"\nАудитория проекта:\n{data['audience']}"
                                               f"\nКак будет работать проект:\n{data['how_work']}"
                                               f"\nОсобенности и отличия проекта:\n{data['differences']}"
                                               f"\nМонетка ннннада!?{data['monetization']}")
    await state.finish()
    await bot.send_message(call.from_user.id, "Появилась новая идея? Пройди опрос еще раз! введи /start",
                           reply_markup=start_idea)


def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(start_idea, commands="start")
    # dp.register_callback_query_handler(start_idea, text="start_idea")
    dp.register_message_handler(about_idea, content_types=["text"], state=FSMInterview.about)
    dp.register_message_handler(problem_idea, content_types=["text"], state=FSMInterview.problem)
    dp.register_message_handler(audience_idea, content_types=["text"], state=FSMInterview.audience)
    dp.register_message_handler(how_work_idea, content_types=["text"], state=FSMInterview.how_work)
    dp.register_message_handler(differences_idea, content_types=["text"], state=FSMInterview.differences)
    dp.register_callback_query_handler(monetization_idea, state=FSMInterview.monetization)






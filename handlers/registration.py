import asyncio
from io import BytesIO

import xlsxwriter as xlsxwriter
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from keyboards import *
from create_bot import bot, Nastya_id
import emoji
import datetime
import time
from aiogram.types import KeyboardButton, ReplyKeyboardRemove
import validators



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
    # if not db.user_exists(int(message.from_user.id)):
        #db.user_exists(int(message.from_user.id))
    await message.answer(f"Привет! Я ExLab Registration Bot!\n" + emoji.emojize(":vulcan_salute:") +
                         f"Я помогу тебе пройти опрос и стать частью команды ExLab!", reply_markup=start_kb_first)
    # else:
    #     await message.answer("Привет!\nТы уже успешно прошел опрос.")


async def start_question(call: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        data["tg_id"] = call.from_user.id
        data["tg_user_name"] = call.from_user.username
    # db.add_user(call.from_user.id, call.from_user.username)
    await FSMAdmin.question_name.set()
    await bot.send_message(call.from_user.id, "Как тебя зовут🖐️?\nВведи фамилию и имя.")


async def question_name(message: types.Message, state=FSMContext):
    # db.set_username(message.from_user.id, message.text)
    async with state.proxy() as data:
        data["name_surename"] = message.text
    await FSMAdmin.next()
    await message.answer(emoji.emojize(":baby:") + "Укажи дату рождения.\n(dd.mm.yyyy)")


async def birth_day(message: types.Message, state=FSMContext):
    try:
        date_correct_dbase_format = datetime.datetime.strptime(message.text, "%d.%m.%Y").strftime("%Y-%m-%d")
        # db.birthday(message.from_user.id, date_correct_dbase_format)
        async with state.proxy() as data:
            data["birthday"] = date_correct_dbase_format
        await FSMAdmin.next()
        await message.answer(emoji.emojize(":cityscape:") + "Откуда ты?\n"
                                                            "Укажи страну и город.")
    except ValueError:
        await FSMAdmin.question_birth.set()
        await bot.send_message(message.from_user.id, "Введите корректную дату в формате: день.месяц.год")


async def question_city(message: types.Message, state=FSMContext):
    # db.set_city(message.from_user.id, message.text)
    async with state.proxy() as data:
        data["city"] = message.text
    await FSMAdmin.next()
    await message.answer(emoji.emojize(":mechanic:") + "Выбери свою специальнось.", reply_markup=kb_speciality)


async def my_speciality(message: types.Message, state=FSMContext):
    # db.set_speciality(message.from_user.id, message.text)
    async with state.proxy() as data:
        data["speciality"] = message.text
    await FSMAdmin.next()
    await message.answer("Расскажи о своем обучении по этой специальности.")


async def question_speciality(call: types.CallbackQuery, state=FSMContext):
    if call.data == "speciality_etc":
        await bot.send_message(call.from_user.id, "Какая у тебя специальность?")
        await FSMAdmin.question_spec_etc.set()
    else:
        # db.set_speciality(call.from_user.id, call.data)
        speciality = call.data[11::]
        async with state.proxy() as data:
            data["speciality"] = speciality
        await FSMAdmin.question_specialization.set()
        await bot.send_message(call.from_user.id, "Расскажи о своем обучении по этой специальности.")


async def question_specialization(message: types.Message, state=FSMContext):
    # db.set_specialization(message.from_user.id, message.text)
    async with state.proxy() as data:
        data["specialization"] = message.text
    await FSMAdmin.next()
    await message.answer(emoji.emojize(":graduation_cap:") + "Какой у тебя стек технологий?")


async def question_courses(message: types.Message, state=FSMContext):
    # db.set_courses(message.from_user.id, message.text)
    async with state.proxy() as data:
        data["courses"] = message.text
    await FSMAdmin.next()
    await message.answer(emoji.emojize(":face_with_tongue:") + "Уровень владения английским?",
                         reply_markup=english_level)


async def eng_lev(call: types.CallbackQuery, state=FSMContext):
    # db.set_eng(call.from_user.id, call.data)
    english = call.data[-2::]
    async with state.proxy() as data:
        data["english"] = english
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
        # db.set_links(message.from_user.id, message.text)
        async with state.proxy() as data:
            data["linkedin"] = message.text
        await FSMAdmin.next()
        await message.answer("Прикрепи ссылку на свое портфолио. Если оно есть.",
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                             .insert(KeyboardButton("Пропустить")))


async def portfolio(message: types.Message, state=FSMContext):
    if message.text == "Пропустить":
        await FSMAdmin.next()
        async with state.proxy() as data:
            data["portfolio"] = "-"
        await message.answer(emoji.emojize(":ear:") + "Как ты узнал об ExLab?\n", reply_markup=source_exlab)
    else:
        if validators.url(message.text) is True:
            # db.set_portfolio(message.from_user.id, message.text)
            async with state.proxy() as data:
                data["portfolio"] = message.text
            await FSMAdmin.next()
            await message.answer(emoji.emojize(":ear:") + "Как ты узнал об ExLab?\n", reply_markup=source_exlab)
        else:
            await message.answer("!Ты ввел некорректный URL!\nПопробуй еще раз.")
            await FSMAdmin.question_portfolio.set()


async def sourse_exlab_etc(message: types.Message, state=FSMContext):
    # db.set_sourse(message.from_user.id, message.text)
    async with state.proxy() as data:
        data["sourse_exlab"] = message.text
    await FSMAdmin.next()
    await message.answer(emoji.emojize(":white_question_mark:") + "Почему ты решил присоединиться "
                                                            "к ExLab?" + emoji.emojize(":white_question_mark:"))


async def sourse_exlab(call: types.CallbackQuery, state=FSMContext):
    if call.data == "source_etc":
        await bot.send_message(call.from_user.id, "Как именно ты о нас узнал?", reply_markup=ReplyKeyboardRemove())
        await FSMAdmin.question_sours_etc.set()
    else:
        # db.set_sourse(call.from_user.id, call.data)
        sourses = call.data[7::]
        async with state.proxy() as data:
            data["sourse_exlab"] = sourses
        await FSMAdmin.question_reason.set()
        await bot.send_message(call.from_user.id, emoji.emojize(":white_question_mark:") +
                               "Почему ты решил присоединиться к ExLab?" + emoji.emojize(":white_question_mark:"),
                               reply_markup=ReplyKeyboardRemove())


async def reason_exlab(message: types.Message, state: FSMContext):
    # db.set_reason(message.from_user.id, message.text)
    async with state.proxy() as data:
        data["reason_exlab"] = message.text
    await FSMAdmin.next()
    await message.answer(emoji.emojize(":gem_stone:") + "У тебя есть идея, которую мы могли бы реализовать вместе?" +
                         emoji.emojize(":gem_stone:"), reply_markup=answer_yes_no)


async def idea_exlab(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['idea'] = call.data
    # db.set_idea(call.from_user.id, call.data)
    # last_user = db.last_user(call.from_user.id)[0]
    await bot.send_message(Nastya_id, text=f"Наcтя появился новый пользователь!!!"
                                           f"\nИмя телеграм юзера: {data['tg_user_name']}"
                                           f"\nИмя Фамилия: {data['name_surename']}"
                                           f"\nДата рождения: {data['birthday']}"
                                           f"\nГород: {data['city']}"
                                           f"\nСпециальность: {data['speciality']}"
                                           f"\nОбучение по специальности: {data['specialization']}"
                                           f"\nСтек технологий: {data['courses']}"
                                           f"\nУровень английского: {data['english']}"
                                           f"\nСсылка на LinkedIn: {data['linkedin']}"
                                           f"\nСсылка на портфолио: {data['portfolio']}"
                                           f"\nКак он нас нашел: {data['sourse_exlab']}"
                                           f"\nПричины: {data['reason_exlab']}"
                                           f"\nНаличие идей: {data['idea']}")
    await state.finish()
    await bot.send_message(call.from_user.id, text="Добро пожаловать в ExLab!\nВ нашей телеграмм-группе ты сможешь "
                                                   "познакомиться с другими участниками проекта.",
                           reply_markup=join_group)
    time.sleep(10)
    await bot.send_message(call.from_user.id, text="Ознакомься с правилами нашего сообщества.", reply_markup=rules)
    time.sleep(10)
    await bot.send_message(call.from_user.id, text="Подписывайся на наши соц сети, чтобы быть в курсе всех новостей "
                                                   "ExLab.", reply_markup=social_media)
    await bot.send_message(call.from_user.id, "Спасибо за регистрацию. Рады, что ты с нами!")
    if call.data == "YES":
        await bot.send_message(call.from_user.id, "Ты сказал что у тебя есть идея!\nРасскажи о своем проекте и мы "
                                                  "поможем найти команду для его реализации.")
    else:
        await bot.send_message(call.from_user.id, "Когда появится идея нажимай кнопку и расскажи о своем проекте и мы "
                                                  "поможем найти команду для его реализации.")

# async def unsubscribe(call: types.CallbackQuery):
#     if call.data == "unsubscribe":
#         db.set_signup(call.from_user.id, False)
#         await call.message.delete()
#         await bot.send_message(call.from_user.id, "Ты отписался от рассылки", reply_markup=del_sub)
#     else:
#         db.set_signup(call.from_user.id, True)
#         await call.message.delete()
#         await bot.send_message(call.from_user.id, "Ты подписался на рассылку", reply_markup=del_unsub)


# async def del_user(message: types.Message):
#     db.user_del(message.from_user.id)
#     await message.delete()
#     await bot.send_message(message.from_user.id, emoji.emojize(":loudly_crying_face:") + "Ты успешно удалил "
#                                                                                          "пользователя!"
#                            + emoji.emojize(":loudly_crying_face:"), reply_markup=start_kb_first)


# async def get_nastia(message: types.Message):
#     await message.answer("А ты хто такой!!!")
#     if message.from_user.id == Nastya_id:
#         try:
#             await bot.send_message(message.from_user.id, "Подождешь...неабсерыШся!!")
#             a = db.all_users()
#             print(a)
#             output = BytesIO()
#             workbook = xlsxwriter.Workbook(output)
#             worksheet = workbook.add_worksheet('Светлые_головы')  # Создание вкладки в exel
#
#             cell_format = workbook.add_format({'bold': True, 'font_color': 'red'})
#             # Создание шапок
#             worksheet.write(0, 0, 'ID телеги', cell_format)
#             worksheet.write(0, 1, 'Имя телеграм юзера', cell_format)
#             worksheet.write(0, 2, 'Имя Фамилия', cell_format)
#             worksheet.write(0, 3, 'Дата рождения', cell_format)
#             worksheet.write(0, 4, 'Город', cell_format)
#             worksheet.write(0, 5, 'Специальность', cell_format)
#             worksheet.write(0, 6, 'Обучение по специальности', cell_format)
#             worksheet.write(0, 7, 'Стек технологий', cell_format)
#             worksheet.write(0, 8, 'Уровень английского', cell_format)
#             worksheet.write(0, 9, 'Ссылка на LinkedIn', cell_format)
#             worksheet.write(0, 10, 'Ссылка на портфолио', cell_format)
#             worksheet.write(0, 11, 'Как он нас нашел', cell_format)
#             worksheet.write(0, 12, 'Причины', cell_format)
#             worksheet.write(0, 13, 'Наличие идей', cell_format)
#
#             worksheet.set_column(0, 13, 30)  # Это форматирование столбцов. Т.е. с 0 по 1 столбец ширина 15 хз чего
#
#             cell_format = workbook.add_format({'bold': False, 'font_color': 'black', 'align': 'left', 'valign': 'top'})
#             date_format = workbook.add_format({'num_format': 'd mmmm yyyy'})
#             # это форматирование
#             cell_format.set_text_wrap()
#             for i in range(1, len(a)):
#                 worksheet.write(i, 0, a[i - 1][0], cell_format)
#                 worksheet.write(i, 1, a[i - 1][1], cell_format)
#                 worksheet.write(i, 2, a[i - 1][2], cell_format)
#                 worksheet.write(i, 3, a[i - 1][3], date_format)
#                 worksheet.write(i, 4, a[i - 1][4], cell_format)
#                 worksheet.write(i, 5, a[i - 1][5], cell_format)
#                 worksheet.write(i, 6, a[i - 1][6], cell_format)
#                 worksheet.write(i, 7, a[i - 1][7], cell_format)
#                 worksheet.write(i, 8, a[i - 1][8], cell_format)
#                 worksheet.write(i, 9, a[i - 1][9], cell_format)
#                 worksheet.write(i, 10, a[i - 1][10], cell_format)
#                 worksheet.write(i, 11, a[i - 1][11], cell_format)
#                 worksheet.write(i, 12, a[i - 1][12], cell_format)
#                 worksheet.write(i, 13, a[i - 1][13], cell_format)
#             workbook.close()
#
#             file = output.getvalue()
#             file_name = f"abracadabra.xlsx"
#             await asyncio.sleep(5)
#
#             await bot.send_document(message.from_user.id, (file_name, file))
#         except:
#             await message.answer("Что-то пошло не так!")
#             workbook.close()
#     else:
#         await message.answer("А ты хто такой!!!")





def register_handlers_registration(dp: Dispatcher):

    dp.register_message_handler(start_program, commands="start")
    # dp.register_message_handler(get_nastia, commands="abracadabra")
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
    # dp.register_message_handler(del_user, commands="beornotbe")
    # dp.register_callback_query_handler(unsubscribe, text_contains="subscribe")

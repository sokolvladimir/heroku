from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client, answer1


# @dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.", reply_markup=answer1)


# @dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    text = "мне плевать!"
    await message.answer(f'"{message.text}" {text}', reply_markup=kb_client)

# эти строки для пошалить ***************


async def my_photo(message: types.Message):
    await message.reply("Это фото")


async def my_video(message: types.Message):
    await message.reply("Это видео")


async def my_doc(message: types.Message):
    await message.reply("Это документ")
# Конец шалости ************

def handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
    dp.register_message_handler(echo)
    dp.register_message_handler(my_photo, content_types=["photo"])
    dp.register_message_handler(my_video, content_types=["video"])
    dp.register_message_handler(my_doc, content_types=["document"])

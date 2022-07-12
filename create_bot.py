import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from db.database import Database

storage = MemoryStorage()
#
# API_TOKEN = '5285312589:AAE2GIOyAAICFL0Ue9m4Qaf7Vj96lKl69FQ'
# Мой токен
API_TOKEN = '5251328379:AAGDkd6xTZan-tCjmyCWU_hjQPEhRDtinWg'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

# db = Database(database='exlabtea_registration', user='exlabtea',
#               password='FieKaek0',
#               host='vh104.hoster.by')

# id Насти оно нужно для того что-бы передовать информацию при появлении нового пользователя
# Nastya_id = 519610702
Nastya_id = 545074878


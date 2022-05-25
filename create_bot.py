import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db.database import Database

storage = MemoryStorage()

API_TOKEN = '5285312589:AAEYTN0vs3yLzYVn0R3iKR2xnX5pvCE_p00'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

db = Database(dbname='d2setupduudqp6', user='hsrqfsvztotzlo',
              password='8ac828c22e62c498e76eca2900d0b1c35ee5576e0ee26c63f641a6fc1378ce17',
              host='ec2-34-231-177-125.compute-1.amazonaws.com')


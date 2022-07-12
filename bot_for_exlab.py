from aiogram import executor
from create_bot import dp
from handlers import registration

registration.register_handlers_registration(dp)
# interview_project.register_handlers_registration(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


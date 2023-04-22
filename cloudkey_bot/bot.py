import os
from aiogram import Bot, Dispatcher, executor, types
from db_connet import SQLiteConnect

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

db = SQLiteConnect('..\\cloudkey\\db.sqlite3')


@dp.message_handler()
async def login_user(message: types.Message):
    await message.answer('Введите логин или email и пароль. Пример: login - pass')


executor.start_polling(dp, skip_updates=True)

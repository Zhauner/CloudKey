import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from db_connect import SQLiteConnect

storage = MemoryStorage()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)

db = SQLiteConnect('..\\cloudkey\\db.sqlite3')
is_login = False
current_user_id = 0


class LoginUser(StatesGroup):
    login = State()
    password = State()


@dp.message_handler(commands=['start'], state=None)
async def start(message: types.Message):
    await LoginUser.login.set()
    await message.answer('Введите логин или email от сайта Cloud[Key]')


@dp.message_handler(state=LoginUser.login)
async def login_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text.strip()
    await LoginUser.next()
    await message.answer('Введите пароль от сайта Cloud[Key]')


@dp.message_handler(state=LoginUser.password)
async def password_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text.strip()

    async with state.proxy() as data:
        user_id = db.pass_and_login_check(data['login'], data['password'])
        if user_id != 'Неверный login(email) или пароль':
            global is_login
            global current_user_id
            is_login = True
            current_user_id = user_id
        else:
            is_login = False
            current_user_id = 0

    await state.finish()


@dp.message_handler(Text('проверка'))
async def check_login_user(message: types.Message):
    if is_login:
        await message.answer('Вы в системе')
        await message.answer(f'Ваш id: {current_user_id}')
    else:
        await message.answer('[+] not logg')


executor.start_polling(dp, skip_updates=True)

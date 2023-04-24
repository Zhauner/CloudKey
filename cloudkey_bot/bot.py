import os
import base64
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup
from db_connect import SQLiteConnect
from PIL import Image
from io import BytesIO

storage = MemoryStorage()

bot = Bot(token=os.getenv('TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

db = SQLiteConnect('..\\cloudkey\\db.sqlite3')
is_login = False
current_user_id = 0


class LoginUser(StatesGroup):
    login = State()
    password = State()


@dp.message_handler(commands=['start'])
async def start_app(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = ['✅ Логин', '🔐 Проверка статуса']
    keyboard.add(*start_button)
    await message.answer('👋')
    await message.answer('Для начала работы авторизуйтесь используя данные с сайта Cloud[Key]', reply_markup=keyboard)


@dp.message_handler(Text(equals='✅ Логин'), state=None)
async def login(message: types.Message):
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
        if user_id:
            global is_login
            global current_user_id
            is_login = True
            current_user_id = user_id

            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            start_menu = ['Меню']
            keyboard.add(*start_menu)

            await message.answer(
                '🟢 Вы успешно авторизованы! 🟢',
                reply_markup=ReplyKeyboardRemove()
            )
            await message.answer('Нажмите кнопку "Меню"', reply_markup=keyboard)
        else:
            is_login = False
            current_user_id = 0
            await message.answer('❌ Неверный логин(email) или пароль ❌')

    await state.finish()


@dp.message_handler(Text(equals='Меню'))
async def menu(message: types.Message):
    if is_login and current_user_id != 0:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        menu_buttons = ['🔶 Мои пароли (Cloud[Key]) 🔶', 'Выйти из системы']
        keyboard.add(*menu_buttons)
        await message.answer('все пункты', reply_markup=keyboard)
    else:
        await message.answer('Вы не авторизованы')


@dp.message_handler(Text(equals='🔶 Мои пароли (Cloud[Key]) 🔶'))
async def show_datas(message: types.Message):
    if is_login and current_user_id != 0:
        data = db.show_datas_by_id(current_user_id)
        for x in data:
            fav = Image.open(BytesIO(base64.b64decode(x[1])))
            fav.save("fav.png")
            img = open("fav.png", "rb")
            await message.answer_photo(img, caption=f'{x[-1]}')
            os.remove('fav.png')
    else:
        await message.answer('Вы не авторизованы')


@dp.message_handler(Text(equals='Выйти из системы'))
async def logout(message: types.Message):
    global is_login
    global current_user_id
    if is_login and current_user_id != 0:
        is_login = False
        current_user_id = 0

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        again_button = ['/start']
        keyboard.add(*again_button)

        await message.answer('Вы успешно вышли из системы!', reply_markup=ReplyKeyboardRemove())
        await message.answer('Войти снова', reply_markup=keyboard)
    else:
        await message.answer('Вы не авторизованы!')


@dp.message_handler(Text(equals='🔐 Проверка статуса'))
async def check_login_user(message: types.Message):
    if is_login:
        await message.answer(f'Вы в системе, Ваш id: {current_user_id}')
    else:
        await message.answer(f'[+] not logg {current_user_id}')


executor.start_polling(dp, skip_updates=True)

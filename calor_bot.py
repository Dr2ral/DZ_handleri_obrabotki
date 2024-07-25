from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())



@dp.message_handler(text=['hi', 'hello', 'привет'])
async def all_massages(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Что бы начать общение с ботом нажмите /start пожалуйста')

@dp.message_handler(commands = ['start'],)
async def start(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer(f'Добро пожаловать {message.from_user.username} Я бот помогающий твоему здоровью')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text=['Calories', 'calories'])
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()
    #await state.finish()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()
    #await state.finish()


@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    await message.answer(f'Для мужчин - {10 * data["weight"] + 6.25 * data["growth"] - 5 * data["age"] + 5}')
    #await message.answer(10 * data["age"] + data["growth"])
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


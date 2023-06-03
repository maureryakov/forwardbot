import openai
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

# Устанавливаем ключ API OpenAI
openai.api_key = "sk-Aq3nc9ZAq7rdiiR6Vh=====================UhRD"

# Инициализируем бота и диспетчер
bot = Bot(token="2102525803:AAED======================Oj00")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Определяем состояния для FSM
class States(StatesGroup):
    waiting_for_pet_type = State()
    waiting_for_pet_size = State()
    waiting_for_food_type = State()

# Обрабатываем команду /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет! Я могу помочь тебе с выбором питания для твоего питомца!")
    await message.answer("Какой у тебя питомец? Кошка или собака?")
    await States.waiting_for_pet_type.set()

# Обрабатываем сообщения с питомцем
@dp.message_handler(state=States.waiting_for_pet_type)
async def process_pet_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["pet_type"] = message.text.lower()
    await message.answer("Какого размера твой питомец? Маленький, средний или большой?")
    await States.waiting_for_pet_size.set()

# Обрабатываем сообщения с размером питомца
@dp.message_handler(state=States.waiting_for_pet_size)
async def process_pet_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["pet_size"] = message.text.lower()
    await message.answer("Какой тип корма ты ищешь?")
    await States.waiting_for_food_type.set()

# Обрабатываем сообщения с типом корма
@dp.message_handler(state=States.waiting_for_food_type)
async def process_food_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["food_type"] = message.text.lower()
    pet_type = data["pet_type"]
    pet_size = data["pet_size"]
    food_type = data["food_type"]
    prompt = f"Рекомендуемый тип корма для {pet_type}, размером {pet_size} - это {food_type}. Почему ты ищешь такой тип корма?"
    await message.answer("Обрабатываем запрос...")
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    answer = response.choices[0].text
    await message.answer(answer)
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

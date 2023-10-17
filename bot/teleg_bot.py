import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from post_generator import PostGenerator
from image_search_download import search_image, download_image
from logging_config import configure_logging
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Настройка логгирования
configure_logging()
logger = logging.getLogger(__name__)

# Получение API-токена из переменных окружения
API_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Определение состояний для машины состояний
class GenerState(StatesGroup):
    prompt = State()


# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: types.Message):
    # Создание клавиатуры для главного меню
    button = [
        [
            types.KeyboardButton(text="👤 Профиль"),
            types.KeyboardButton(text="🔄 Генерировать"),
            types.KeyboardButton(text="ℹ️Информация")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer("Выберите пункт в меню: ", reply_markup=keyboard)


# Обработчик выбора "👤 Профиль"
@dp.message(F.text == "👤 Профиль")
async def user_profile(message: types.Message):
    # Отправка информации о профиле пользователя
    user_id = message.from_user.id
    username = message.from_user.username
    await message.answer(f"ID: {user_id}\nНикнейм: {username}")


# Обработчик выбора "ℹ️Информация"
@dp.message(F.text == "ℹ️Информация")
async def about(message: types.Message):
    # Отправка информации о боте
    telegram = "@example"
    mail = "example@example.com"
    info = "Бот предоставляет доступ к быстрой генерации контента."
    await message.answer(f"telegram: {telegram}\nmail: {mail}\ninfo: {info}")


# Обработчик выбора "🔄 Генерировать"
@dp.message(F.text == "🔄 Генерировать")
async def generate(message: types.Message, state: FSMContext):
    # Начало процесса генерации контента
    await message.answer("Введите запрос для генерации контента."
                         "\nНапример: Cгенерируй пост про космос")
    await state.set_state(GenerState.prompt)


# Обработчик ввода текста для генерации контента
@dp.message(GenerState.prompt, F.text)
async def on_text(message: types.Message, state: FSMContext):
    try:
        await message.answer("Ожидайте, генерации поста занимает около 30 секунд...")
        user_prompt = message.text
        generator = PostGenerator()
        generated_text, keywords = generator.generate_post(user_prompt)

        if generated_text:
            # Поиск и загрузка изображения
            image_url = await search_image(keywords)

            if image_url:
                filename = await download_image(image_url)
                await bot.send_photo(message.chat.id,
                                     photo=FSInputFile(filename),
                                     caption=generated_text)
                await state.clear()
            else:
                await message.reply('Изображение не найдено.')
        else:
            await message.reply('Не удалось сгенерировать текст поста.')
    except Exception as error_message:
        logging.error(f'Произошла ошибка: {error_message}')
        await message.reply(f'Произошла ошибка: {error_message}')


# Основная функция для запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

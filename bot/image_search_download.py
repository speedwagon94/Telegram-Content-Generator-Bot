import uuid
import os
import logging
import aiohttp
import aiofiles
from logging_config import configure_logging
from dotenv import load_dotenv


load_dotenv()

configure_logging()
logger = logging.getLogger(__name__)


async def search_image(query):
    """
    Выполняет поиск изображения по запросу.

    :param query: Запрос для поиска изображения.
    :return: URL найденного изображения или сообщение об ошибке.
    """
    api_key = os.getenv('API_KEY_GOOGLE')
    cx = os.getenv('API_CX_GOOGLE')
    url = f'https://www.googleapis.com/customsearch/v1?cx={cx}&key={api_key}&q={query}&searchType=image'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if 'items' in data and len(data['items']) > 0:
                    image_url = data['items'][0]['link']
                    return image_url
                else:
                    logging.error('Изображение не найдено')
                    return 'Изображение не найдено'
            else:
                error_message = f'Некорректный статус-код: {response.status}'
                logging.error(error_message)
                return error_message


async def download_image(image_url):
    """
    Загружает изображение по URL.

    :param image_url: URL изображения для загрузки.
    :return: Путь к сохраненному файлу или сообщение об ошибке.
    """
    if not os.path.exists('images'):
        os.makedirs('images')  # Создаем папку для изображений, если её нет

    # Генерируем уникальное имя файла
    filename = f'images/{uuid.uuid4()}.jpg'

    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status == 200:
                async with aiofiles.open(filename, 'wb') as file:
                    await file.write(await response.read())
                return filename
            else:
                error_message = f'Некорректный статус-код при загрузке изображения: {response.status}'
                logging.error(error_message)
                return error_message

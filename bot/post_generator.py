import os
import logging
import openai
from logging_config import configure_logging
from dotenv import load_dotenv


load_dotenv()

configure_logging()
logger = logging.getLogger(__name__)


class PostGenerator:
    def __init__(self):
        """
        Конструктор класса PostGenerator.
        """
        openai.api_key = os.getenv('API_KEY_GPT')
        self.model = 'gpt-3.5-turbo'

    def generate_text(self, prompt):
        """
        Генерирует текст на основе заданного промпта.

        Args:
            prompt (str): Промпт для генерации текста.

        Returns:
            str: Сгенерированный текст.

        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': 'Сгенирируй пост неболее 200 символов про ' + prompt},
                ]
            )

            if response and 'choices' in response and len(response['choices']) > 0:
                text = response['choices'][0]['message']['content'].strip()
                return text
            else:
                logging.error('Ошибка при генерации текста')
        except Exception as e:
            logging.error(f'Ошибка при запросе к OpenAI: {e}')

    def generate_post(self, user_prompt):
        """
        Генерирует пост на основе пользовательского промпта.

        Args:
            user_prompt (str): Промпт, предоставленный пользователем.

        Returns:
            tuple: Кортеж, содержащий сгенерированный текст и ключевые слова.

        """
        generated_text = self.generate_text(user_prompt)

        if generated_text:
            keywords = self.extract_keywords(generated_text)
            return generated_text, keywords

    def extract_keywords(self, post):
        """
        Извлекает ключевые слова из сгенерированного поста.

        Args:
            post (str): Сгенерированный пост.

        Returns:
            str: Ключевые слова, связанные с постом.

        """
        prompt = f'Write down the keyword in English for an accurate image search. ' \
                 f'The word should explicitly describe the essence of the entire post. ' \
                 f'In order to find the right image for this word, write only the WORD ITSELF, ' \
                 f'without the hashtag and so on. Just the word and thats it: {post}'
        return self.generate_text(prompt)

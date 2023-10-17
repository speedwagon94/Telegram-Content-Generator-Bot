import logging


def configure_logging():
    """
    Настройка системы логгирования.

    Эта функция устанавливает настройки логгирования для приложения.
    Она определяет формат сообщений, уровень логгирования
    (в данном случае, INFO), и файл, в который будут записываться логи.

    Returns:
        None
    """
    # Определяем формат сообщений логгирования,
    # дату и время, имя логгера, уровень и текст сообщения.
    log_format = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"

    # Устанавливаем основные настройки логгирования,
    # включая уровень логгирования (INFO) и формат сообщений.
    logging.basicConfig(level=logging.INFO, format=log_format)

    # Определяем имя файла для записи логов.
    log_file = "app.log"

    # Создаем обработчик логгирования для записи логов в файл.
    file_handler = logging.FileHandler(log_file)

    # Устанавливаем формат сообщений в обработчике, соответствующий ранее определенному log_format.
    file_handler.setFormatter(logging.Formatter(log_format))

    # Устанавливаем уровень логгирования для обработчика (INFO).
    file_handler.setLevel(logging.INFO)

    # Получаем корневой логгер, который обрабатывает все сообщения логгирования.
    root_logger = logging.getLogger()

    # Добавляем обработчик (file_handler) к корневому логгеру.
    root_logger.addHandler(file_handler)

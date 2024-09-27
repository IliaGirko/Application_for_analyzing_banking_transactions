import json
import logging
import os
import re
from typing import Any

import pandas as pd
from dotenv import load_dotenv

logger = logging.getLogger("services.py")
logger.setLevel(logging.DEBUG)
logger_handler = logging.FileHandler("main.log", "a")
logger_formatter = logging.Formatter(
    "Time: %(asctime)s Module name: %(name)s Level message: %(levelname)s Message: %(message)s"
)
logger_handler.setFormatter(logger_formatter)
logger.addHandler(logger_handler)

load_dotenv()

path_to_file: str = os.getenv("PATH_TO_FILE")


def simple_search(user_input_simple_search: str) -> list[dict[Any]] | str:
    """Функция выполняющая простой поиск"""
    try:
        logger.info("Запуск функции simple_search")
        json_file = json.loads(pd.read_excel(path_to_file).to_json(indent=4, force_ascii=False, orient="records"))
        result = []
        for file in json_file:
            search_str_info = re.findall(user_input_simple_search, file.get("Описание"), flags=re.IGNORECASE)
            if search_str_info:
                result.append(file)
            if file.get("Категория"):
                search_str_category = re.findall(user_input_simple_search, file.get("Категория"), flags=re.IGNORECASE)
                if search_str_category:
                    result.append(file)
        logger.info("Информация отобрана")
        if result == []:
            logger.error(f"По слову {user_input_simple_search} операций не найдено")
            return f"По заданному слову {user_input_simple_search} не найдено операций"
        logger.info("Вывод результата")
        return result
    except Exception as error:
        logger.error(f"Программа завершила работу с ошибкой: {error}")
        return f"{error}"

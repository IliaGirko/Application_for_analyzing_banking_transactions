import json
import logging
import os
from datetime import datetime
from typing import Any

import pandas as pd
from dotenv import load_dotenv

from reports import spending_by_category
from services import simple_search
from views import file_with_expenses_for_the_period

logger = logging.getLogger("main.py")
logger.setLevel(logging.DEBUG)
logger_handler = logging.FileHandler("main.log", "a")
logger_formatter = logging.Formatter(
    "Time: %(asctime)s Module name: %(name)s Level message: %(levelname)s Message: %(message)s"
)
logger_handler.setFormatter(logger_formatter)
logger.addHandler(logger_handler)

load_dotenv()

path_to_file: str = os.getenv("PATH_TO_FILE")
transactions_data_frame: pd.DataFrame = pd.read_excel(path_to_file)


def main():
    """Функция запуска основной логики программы"""
    try:
        logger.info("Запуск основной логики программы в функции main")
        now_time: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result_expenses_for_the_period: pd.DataFrame = file_with_expenses_for_the_period(now_time)
        result_home_pages: list[dict[Any]] = json.dumps(result_expenses_for_the_period, indent=4, ensure_ascii=False)
        logger.info("Вывод работы 'Веб-страницы' - страница 'Главная'")
        print(f"'Веб-страницы' - страница 'Главная': \n{result_home_pages}")
        logger.info("Вывод работы страница 'Сервисы' - Простой поиск")
        print("Страница 'Сервисы' - Простой поиск:")
        print(simple_search(input("Введите слово для поиска: ").title()))
        logger.info("Вывод работы страницы 'Отчеты' - Траты по категории")
        print("Страница 'Отчеты' - Траты по категории: ")
        category: str = input("Введите категорию для сортировки: ")
        date: str = input("Введите дату в формате ДД.ММ.ГГГГ: ")
        print(spending_by_category(transactions_data_frame, category, date))
        logger.info("Завершение основной логики программы")
    except Exception as error:
        logger.error(f"Ошибка: {error}")
        print(error)


print(main())

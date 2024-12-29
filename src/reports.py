import datetime
import logging
import os
from functools import wraps
from typing import Any, Callable

import pandas as pd
from dotenv import load_dotenv

logger = logging.getLogger("reports.py")
logger.setLevel(logging.DEBUG)
logger_handler = logging.FileHandler("main.log", "a")
logger_formatter = logging.Formatter(
    "Time: %(asctime)s Module name: %(name)s Level message: %(levelname)s Message: %(message)s"
)
logger_handler.setFormatter(logger_formatter)
logger.addHandler(logger_handler)

load_dotenv()

path_to_file: str = os.getenv("PATH_TO_FILE")


def log(filename: str | None = "decorator.txt") -> Callable:
    """Декоратор который автоматически регистрирует детали выполнения функций, такие как время вызова,
    имя функции, передаваемые аргументы, результат выполнения и информацию об ошибках"""

    def wrapper(spending_by_category: Callable) -> Callable:
        @wraps(spending_by_category)
        def inner(*args: Any, **kwargs: Any) -> Any:
            logger.info("Запуск декоратора log")
            result: Callable = spending_by_category(*args, **kwargs)
            logger.info(f"Записываем результат работы функции spending_by_category в файл {filename}")
            with open(filename, "w+", encoding="UTF-8") as file:
                file.write(f"{result}")

            logger.info("Завершение работы декоратора log")
            return result

        return inner

    return wrapper


@log(filename="mylog.txt")
def spending_by_category(transactions: pd.DataFrame, category: str, date: str = None) -> list[dict[Any]] | str:
    """Функция формирует отчет "траты по категориям" по заданной пользователем категории,
    в период за 3 месяца от указанной пользователем даты. Если дата отсутствует, то берется текущая дата"""
    logger.info("Запуск функции spending_by_category")
    try:
        if date:
            date = datetime.datetime.strptime(date, "%d.%m.%Y")
        else:
            logger.info("Дата не введена, используется сегодняшняя дата")
            date = datetime.datetime.now()
        three_months_ago = date - datetime.timedelta(days=90)
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
        logger.info("Фильтрация данных по категории и дате")
        filtered_transactions = transactions[
            (transactions["Дата операции"] <= date)
            & (transactions["Дата операции"] >= three_months_ago)
            & (transactions["Категория"] == category)
        ]
        if not filtered_transactions.empty:
            logger.info("Вывод результата фильтрации")
            filtered_transactions["Дата операции"] = filtered_transactions["Дата операции"].dt.strftime(
                "%d.%m.%Y %H:%M:%S"
            )
            output = filtered_transactions[["Дата операции", "Сумма операции", "Категория"]]
            return output.to_json(indent=4, force_ascii=False, orient="records")
        else:
            logger.error(f"В заданный период не было операций по категории {category}")
            return (
                f"по заданным параметрам на дату {datetime.datetime.strftime(date, '%d.%m.%Y')} "
                f"в категории {category} нет информации"
            )
    except Exception as error:
        logger.error(f"Программа завершила работу с ошибкой: {error}")
        return f"{error}"

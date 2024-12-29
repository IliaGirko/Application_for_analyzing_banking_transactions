import logging
from typing import Any

from utils import (data_s_and_p, exchange_rate_dollar, exchange_rate_euro, filter_data_card_user, read_excel_file,
                   top_transactions_by_payment_amount, user_greeting)

logger = logging.getLogger("views.py")
logger.setLevel(logging.DEBUG)
logger_handler = logging.FileHandler("main.log", "a")
logger_formatter = logging.Formatter(
    "Time: %(asctime)s Module name: %(name)s Level message: %(levelname)s Message: %(message)s"
)
logger_handler.setFormatter(logger_formatter)
logger.addHandler(logger_handler)


def file_with_expenses_for_the_period(date: str) -> dict[Any | list[dict[str | Any]]] | str:
    """Функция которая принимает на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращает сконсолидированный ответ по странице Главная"""
    try:
        logger.info("Запуск функции file_with_expenses_for_the_period")
        hello: str = user_greeting(date)

        cards_info: list[dict[Any]] = filter_data_card_user(read_excel_file(), date)
        top_transactions: list[dict[Any]] = top_transactions_by_payment_amount(read_excel_file())

        currency_rate_euro: dict[Any] = exchange_rate_euro()
        currency_rate_dollar: dict[Any] = exchange_rate_dollar()
        currency_rates: list[dict[Any]] = [
            {"currency": "USD", "rate": round(currency_rate_dollar.get("rates").get("RUB"), 2)},
            {"currency": "EUR", "rate": round(currency_rate_euro.get("rates").get("RUB"), 2)},
        ]
        s_and_p_data: dict[str | float] = data_s_and_p()
        logger.info("Формирование результата работы функции file_with_expenses_for_the_period")
        json_answer: dict[Any | list[dict[str | Any]]] = {
            "greeting": hello,
            "cards": cards_info,
            "top_transactions": top_transactions,
            "currency_rates": currency_rates,
            "stock_prices": [
                {"stock": "AAPL", "price": s_and_p_data.get("AAPL")},
                {"stock": "AMZN", "price": s_and_p_data.get("AMZN")},
                {"stock": "GOOGL", "price": s_and_p_data.get("GOOGL")},
                {"stock": "MSFT", "price": s_and_p_data.get("MSFT")},
                {"stock": "TSLA", "price": s_and_p_data.get("TSLA")},
            ],
        }
        logger.info("Вывод результата работы функции file_with_expenses_for_the_period")
        return json_answer
    except Exception as error:
        logger.error(f"Ошибка: {error}")
        return f"{error}"

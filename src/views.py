import json
import logging
import os
from datetime import datetime
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

logger = logging.getLogger("views.py")
logger.setLevel(logging.DEBUG)
logger_handler = logging.FileHandler("main.log", "a")
logger_formatter = logging.Formatter(
    "Time: %(asctime)s Module name: %(name)s Level message: %(levelname)s Message: %(message)s"
)
logger_handler.setFormatter(logger_formatter)
logger.addHandler(logger_handler)

load_dotenv()

path_to_file: str = os.getenv("PATH_TO_FILE")
api_key_currency: str = os.getenv("API_KEY_CURRENCY")
api_key_sp: str = os.getenv("API_KEY_SP500")
headers: dict[str] = {"apikey": api_key_currency}
payload: dict = {}


def read_excel_file() -> pd.DataFrame | str:
    """Функция читает данные из excel файла и возвращает DataFrame"""
    try:
        logger.info("Запуск функции read_excel_file")
        logger.info("Производится чтение файла")
        data_frame: pd.DataFrame = pd.read_excel(path_to_file)
        return data_frame
    except Exception as error:
        logger.error(f"Ошибка: {error}")
        return f"{error}"


def filter_data_card_user(dictionary: pd.DataFrame, date: str) -> list[dict[Any]] | str:
    """Функция которая по каждой карте предоставляет данные:
    последние 4 цифры карты,общая сумма расходов, кешбэк (1 рубль на каждые 100 рублей)."""
    try:
        logger.info("Запуск функции filter_data_card_user")
        date_string_dt_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
        start_date_for_sorting = date_string_dt_obj.replace(day=1)
        dictionary["Дата операции"] = dictionary["Дата операции"].apply(
            lambda x: datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
        )
        logger.info("Фильтрация данных")
        filtered_df_by_date: pd.DataFrame = dictionary.loc[
            (dictionary["Дата операции"] <= date_string_dt_obj)
            | (dictionary["Дата операции"] == "2021-12-31") & (dictionary["Дата операции"] >= start_date_for_sorting)
            | (dictionary["Дата операции"] == "2021-12-01")
            & (dictionary["Номер карты"].notnull())
            & (dictionary["Статус"] != "FAILED")
        ]
        grouped_df: pd.DataFrame = filtered_df_by_date.groupby(["Номер карты"], as_index=False).agg(
            {"Сумма операции": "sum"}
        )
        result_data_dict: list = []
        logger.info("Формирование ответа")
        for index, row in grouped_df.iterrows():
            data_dict: dict = {
                "last_digits": row["Номер карты"].replace("*", ""),
                "total_spent": round(row["Сумма операции"], 2),
                "cashback": round(row["Сумма операции"] / 100, 2),
            }
            result_data_dict.append(data_dict)
        logger.info("Вывод результата работы функции filter_data_card_user")
        return result_data_dict
    except Exception as error:
        logger.error(f"Ошибка: {error}")
        return f"{error}"


def user_greeting(time_now: str) -> str:
    """Функция приветствующая пользователя в зависимости от времени"""
    logger.info("Запуск функции user_greeting")
    if 12 > int(time_now[11:13]) > 7:
        logger.info("Вывод приветствия пользователя")
        return "Доброе утро"
    elif 17 > int(time_now[11:13]) > 11:
        logger.info("Вывод приветствия пользователя")
        return "Добрый день"
    elif 22 > int(time_now[11:13]) > 16:
        logger.info("Вывод приветствия пользователя")
        return "Добрый вечер"
    else:
        logger.info("Вывод приветствия пользователя")
        return "Доброй ночи"


def top_transactions_by_payment_amount(dictionary: pd.DataFrame) -> str | list[dict[Any]]:
    """Функция которая выводит данные по топ-5 транзакций по сумме платежа"""
    try:
        logger.info("Запуск функции top_transactions_by_payment_amount")
        logger.info("Фильтрация данных")
        filtered_df_by_sum: pd.DataFrame = dictionary.loc[
            (dictionary["Номер карты"].notnull()) & (dictionary["Статус"] == "OK")
        ]
        logger.info("Отбор топ-5 транзакций по сумме")
        grouped_df: pd.DataFrame = filtered_df_by_sum.sort_values(by="Сумма операции", ascending=False).head()
        result_data_dict: list = []
        logger.info("Подготовка ответа")
        for index, row in grouped_df.iterrows():
            data_dict: dict = {
                "date": row["Дата операции"][:10],
                "amount": round(row["Сумма операции"], 2),
                "category": row["Категория"],
                "description": row["Описание"],
            }
            result_data_dict.append(data_dict)
        logger.info("Вывод результата работы программы top_transactions_by_payment_amount")
        return result_data_dict
    except Exception as error:
        logger.error(f"Ошибка: {error}")
        return f"{error}"


def exchange_rate_euro() -> dict[Any] | str:
    """Функция которая возвращает курс валюты евро"""
    try:
        logger.info("Запуск функции exchange_rate_euro")
        logger.info("Запрос курса евро")
        url_euro: str = "https://api.apilayer.com/fixer/latest?symbols=RUB&base=EUR"
        response = requests.get(url=url_euro, headers=headers, data=payload)
        logger.info("Вывод результата работы функции exchange_rate_euro")
        return response.json()
    except Exception as error:
        logger.error(f"Ошибка: {error}")
        return f"{error}"


def exchange_rate_dollar() -> dict[Any] | str:
    """Функция которая возвращает курс валюты доллар"""
    try:
        logger.info("Запуск функции exchange_rate_dollar")
        logger.info("Запрос курса доллара")
        url_dollar = "https://api.apilayer.com/fixer/latest?symbols=RUB&base=USD"
        response = requests.get(url=url_dollar, headers=headers, data=payload)
        logger.info("Вывод результата работы функции exchange_rate_dollar")
        return response.json()
    except Exception as error:
        logger.error(f"Ошибка: {error}")
        return f"{error}"


def data_s_and_p() -> dict[str | float]:
    """Функция которая возвращает стоимость акций из S&P 500"""
    try:
        logger.info("Запуск функции data_s_and_p")
        logger.info("Чтение файла пользовательских настроек отображение акций")
        with open("../user_settings.json", "r", encoding="UTF-8") as file:
            data_search = json.load(file)
        result_dict: dict = {}
        logger.info("Запрос курса акций на сайт alphavantage.co")
        for user_stock in data_search.get("user_stocks"):
            url: str = (
                f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={user_stock}&apikey={api_key_sp}"
            )
            response = requests.get(url)
            result = response.json()
            key: str = result.get("Meta Data").get("3. Last Refreshed")
            value: str = result.get("Time Series (Daily)").get(key).get("1. open")
            result_dict[user_stock] = round(float(value), 2)
        logger.info("Вывод результата работы функции data_s_and_p")
        return result_dict
    except Exception as error:
        logger.error(f"Ошибка: {error}")
        print(f"{error}")
        return result_dict


def file_with_expenses_for_the_period(date: str) -> dict[Any | list[dict[str | Any]]] | str:
    """Функция которая принимает на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращает сконсолидированный ответ по странице Главная"""
    try:
        logger.info("Запуск функции file_with_expenses_for_the_period")
        ps: str = user_greeting(date)

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
            "greeting": ps,
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

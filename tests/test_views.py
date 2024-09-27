import datetime
import os
from unittest.mock import patch

import pandas as pd
from dotenv import load_dotenv

from src.views import (data_s_and_p, exchange_rate_dollar, exchange_rate_euro, file_with_expenses_for_the_period,
                       filter_data_card_user, read_excel_file, top_transactions_by_payment_amount, user_greeting)

load_dotenv()

path_to_file = os.getenv("PATH_TO_FILE")
data_frames = pd.read_excel(path_to_file)
data_frame = data_frames[:2]
data_frame_1 = data_frames[:6]


@patch("src.views.user_greeting")
def test_user_greeting_night(mock_now):
    mock_now.return_value = datetime.datetime(2022, 1, 1, 5, 14, 18)
    assert user_greeting(mock_now) == "Доброй ночи"


@patch("src.views.user_greeting")
def test_user_greeting_morning(mock_today):
    mock_today.return_value = datetime.datetime(2022, 10, 10, 9, 14, 18)
    assert user_greeting(mock_today) != "Доброе утро"


def test_read_excel_file():
    read_excel_file()


def test_filter_data_card_user():
    assert filter_data_card_user(data_frame, "2024-09-24 11:30:00") == [
        {"last_digits": "7197", "total_spent": -224.89, "cashback": -2.25}
    ]


def test_top_transactions_by_payment_amount():
    assert top_transactions_by_payment_amount(data_frame_1) == [
        {
            "amount": -64.0,
            "category": "Супермаркеты",
            "date": "31.12.2021",
            "description": "Колхоз",
        },
        {
            "amount": -78.05,
            "category": "Супермаркеты",
            "date": "31.12.2021",
            "description": "Колхоз",
        },
        {
            "amount": -118.12,
            "category": "Супермаркеты",
            "date": "31.12.2021",
            "description": "Магнит",
        },
        {
            "amount": -160.89,
            "category": "Супермаркеты",
            "date": "31.12.2021",
            "description": "Колхоз",
        },
        {
            "amount": -564.0,
            "category": "Различные товары",
            "date": "31.12.2021",
            "description": "Ozon.ru",
        },
    ]


@patch("requests.get")
def test_exchange_rate_euro(mock_rates):
    mock_rates.return_value.json.return_value = {
        "Дата операции": "09.07.2018 18:29:03",
        "Сумма операции": -60.0,
        "Категория": "Duty Free",
    }
    assert exchange_rate_euro() == {
        "Дата операции": "09.07.2018 18:29:03",
        "Сумма операции": -60.0,
        "Категория": "Duty Free",
    }


@patch("requests.get")
def test_exchange_rate_dollar(mock_rates):
    mock_rates.return_value.json.return_value = {
        "Дата операции": "09.07.2018 18:29:03",
        "Сумма операции": -60.0,
        "Категория": "Duty Free",
    }
    assert exchange_rate_dollar() == {
        "Дата операции": "09.07.2018 18:29:03",
        "Сумма операции": -60.0,
        "Категория": "Duty Free",
    }


@patch("requests.get")
def test_data_s_and_p(mock_rates):
    mock_rates.return_value.json.return_value = {
        "Meta Data": {
            "1. Information": "Daily Prices (open, high, low, close) and Volumes",
            "2. Symbol": "AAPL",
            "3. Last Refreshed": "2024-09-24",
            "4. Output Size": "Compact",
            "5. Time Zone": "US",
        },
        "Time Series (Daily)": {
            "2024-09-24": {
                "1. open": "228.6450",
                "2. high": "229.3500",
                "3. low": "225.7300",
                "4. close": "227.3700",
                "5. volume": "43556068",
            }
        },
    }
    assert data_s_and_p() == {"AAPL": 228.65, "AMZN": 228.65, "GOOGL": 228.65, "MSFT": 228.65, "TSLA": 228.65}


def test_file_with_expenses_for_the_period():
    assert file_with_expenses_for_the_period("09.07.2018 18:29:03") != {
        "cards": "time data '09.07.2018 18:29:03' does not match format '%Y-%m-%d %H:%M:%S'",
        "currency_rates": [
            {
                "currency": "USD",
                "rate": 92.78,
            },
            {
                "currency": "EUR",
                "rate": 103.37,
            },
        ],
        "greeting": "Добрый вечер",
        "stock_prices": [
            {
                "price": 227.3,
                "stock": "AAPL",
            },
            {
                "price": 194.31,
                "stock": "AMZN",
            },
            {
                "price": 163.64,
                "stock": "GOOGL",
            },
            {
                "price": 435.08,
                "stock": "MSFT",
            },
            {
                "price": 260.6,
                "stock": "TSLA",
            },
        ],
        "top_transactions": [
            {
                "amount": 174000.0,
                "category": "Пополнения",
                "date": "30.12.2021",
                "description": "Пополнение через Газпромбанк",
            },
            {
                "amount": 150000.0,
                "category": "Пополнения",
                "date": "30.07.2018",
                "description": "Пополнение. Перевод средств с торгового счета",
            },
            {
                "amount": 150000.0,
                "category": "Переводы",
                "date": "23.10.2018",
                "description": "Пополнение счета",
            },
            {
                "amount": 138284.27,
                "category": "Переводы",
                "date": "22.02.2019",
                "description": "Вывод средств с брокерского счета",
            },
            {
                "amount": 120000.0,
                "category": "Переводы",
                "date": "30.09.2020",
                "description": "Игорь Б.",
            },
        ],
    }

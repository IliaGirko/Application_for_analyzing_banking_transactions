from src.views import file_with_expenses_for_the_period



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

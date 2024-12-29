import os

import pandas as pd
from dotenv import load_dotenv

from src.reports import spending_by_category

load_dotenv()
path_to_file = os.getenv("PATH_TO_FILE")
df = pd.read_excel("data/operations.xlsx")


def test_spending_by_category():
    assert spending_by_category(df, "Duty Free", "01.09.2018") == (
        "[\n"
        "    {\n"
        '        "Дата операции":"09.07.2018 18:29:03",\n'
        '        "Сумма операции":-60.0,\n'
        '        "Категория":"Duty Free"\n'
        "    }\n"
        "]"
    )


def test_spending_by_category_bag_date():
    assert (
        spending_by_category(df, "Duty Free", "24.09.2024")
        == "по заданным параметрам на дату 24.09.2024 в категории Duty Free нет информации"
    )


def test_spending_by_category_error():
    assert (
        spending_by_category(df, "Dasxcsa", "32.13.2020") == "time data '32.13.2020' does not match format '%d.%m.%Y'"
    )

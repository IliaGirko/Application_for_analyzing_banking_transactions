from src.services import simple_search


def test_simple_search():
    assert simple_search("Duty Freeуу") == "По заданному слову Duty Freeуу не найдено операций"

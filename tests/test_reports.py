from src.reports import spending_by_workday


def test_spending_by_workday(sample_transactions):
    """Тест для функции spending_by_workday"""
    result = spending_by_workday(sample_transactions, date="2025-11-08")

    # Проверяем, что ключи workday и weekend есть
    assert "workday" in result
    assert "weekend" in result

    # Проверяем расчёт средних значений, округляя до двух знаков
    assert round(result["workday"], 2) == 225.0
    assert round(result["weekend"], 2) == 233.33

import json
from unittest.mock import MagicMock, patch

from src.services import profitable_categories


def test_profitable_categories_mock(sample_data):
    # Мокаем json_logger, чтобы не писать логи
    with patch("src.services.json_logger") as mock_logger:
        mock_logger.info = MagicMock()

        # Вызываем функцию
        result_json = profitable_categories(sample_data, 2021, 12)
        result = json.loads(result_json)

        # Проверяем результат
        assert "Ж/д билеты" in result
        assert result["Ж/д билеты"] == 181
        assert "Развлечения" not in result


def test_profitable_categories_empty(empty_transactions):
    """Проверка пустого результата"""
    result_json = profitable_categories(empty_transactions, 2021, 12)
    result = json.loads(result_json)

    assert result == {}

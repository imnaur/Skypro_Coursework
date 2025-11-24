import json
from unittest.mock import patch

import pandas as pd

from src.services import profitable_categories


def test_profitable_categories_mock(sample_data):
    """Тест проверяет работоспособность функции на выгодные кэшбэки."""
    # Сохраняем оригинальные функции
    original_to_datetime = pd.to_datetime
    original_to_numeric = pd.to_numeric

    with patch("pandas.to_datetime") as mock_to_datetime, patch("pandas.to_numeric") as mock_to_numeric:

        # Вызываем оригинальные функции внутри side_effect
        mock_to_datetime.side_effect = lambda x, **kwargs: original_to_datetime(x, format="%d.%m.%Y %H:%M:%S")
        mock_to_numeric.side_effect = lambda x, **kwargs: original_to_numeric(x)

        result_json = profitable_categories(sample_data, 2021, 12)
        result = json.loads(result_json)

        # Проверяем результат
        assert "Ж/д билеты" in result
        assert result["Ж/д билеты"] == 181
        assert "Развлечения" not in result

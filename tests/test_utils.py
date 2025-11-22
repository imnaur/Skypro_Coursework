import pytest

from src.utils import get_greeting, get_top_transactions, process_cards


def test_process_cards(sample_df):
    result = process_cards(sample_df)
    assert isinstance(result, list)
    assert all("last_digits" in card and "total_spent" in card and "cashback" in card for card in result)
    assert any(card["last_digits"] == "1234" for card in result)


def test_get_top_transactions(sample_df):
    top = get_top_transactions(sample_df)
    assert len(top) <= 5
    assert top[0]["amount"] == 2000


@pytest.mark.parametrize(
    "input_time, expected_greeting",
    [
        ("2025-01-20 06:00:00", "Доброе утро!"),
        ("2025-01-20 14:00:00", "Добрый день!"),
        ("2025-01-20 19:00:00", "Добрый вечер!"),
        ("2025-01-20 03:00:00", "Доброй ночи!"),
    ],
)
def test_get_greeting(input_time, expected_greeting):
    assert get_greeting(input_time) == expected_greeting


def test_read_user_settings(sample_settings):
    from src import utils

    settings = utils.read_user_settings(sample_settings)
    assert "user_currencies" in settings
    assert settings["user_currencies"] == ["USD", "EUR"]

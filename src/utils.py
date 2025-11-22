import json
import logging
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

# Логер для функциий()
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_folder = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(log_folder, exist_ok=True)

LOG_FILE = os.path.join(log_folder, "utils.log")

# Создание логера
json_logger = logging.getLogger(__name__)
json_logger.setLevel(logging.DEBUG)

# Обработка файла
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Формат сообщений
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Добавление обработчика
json_logger.addHandler(file_handler)


# Загрузка токена из файла .env
load_dotenv()

CURRENCY_API_KEY = os.getenv("CURRENCYLAYER_KEY")
STOCK_API_KEY = os.getenv("MARKETSTACK_KEY")


def read_excel():
    """Читает файл operations.xlsx из папки data."""
    data_path = Path(__file__).parent.parent / "data" / "operations.xlsx"
    if not data_path.exists():
        json_logger.error(f"Файл не найден: {data_path}")
        raise FileNotFoundError(f"{data_path} not found")

    df = pd.read_excel(data_path, engine="openpyxl")

    json_logger.info(f"Считан файл Excel: {data_path}")
    json_logger.info(f"Количество строк в Excel: {len(df)}")
    return df


def read_user_settings(path: Path = None):
    """Функция читает настройки пользователя из user_settings.json."""
    if path is None:
        path = Path(__file__).parent.parent / "user_settings.json"
    if not path.exists():
        json_logger.error(f"Файл настроек не найден: {path}")
        raise FileNotFoundError(f"{path} not found")
    with open(path, "r", encoding="utf-8") as f:
        settings = json.load(f)
    json_logger.info(f"Файл настроек считан: {path}")
    json_logger.info(f"Настройки пользователя: {settings}")
    return settings


def get_currency_rates(currencies):
    """Получение курсов валют через Currencylayer API."""
    url = "http://api.currencylayer.com/live"
    json_logger.info(f"Запрос курсов валют: {currencies} к {url}")

    try:
        response = requests.get(url, params={"access_key": CURRENCY_API_KEY, "currencies": ",".join(currencies)})
        response.raise_for_status()
        data = response.json()
        json_logger.info(f"Получены курсы валют: {data}")
        return data
    except requests.RequestException as e:
        json_logger.error(f"Ошибка при получении курсов валют: {e}")
        return {}


def get_stock_prices(stocks):
    """Получение цен акций через Marketstack API."""
    url = "https://api.marketstack.com/v1/eod"
    json_logger.info(f"Запрос цен акций: {stocks} к {url}")

    try:
        response = requests.get(url, params={"access_key": STOCK_API_KEY, "symbols": ",".join(stocks)})
        response.raise_for_status()  # проверка на ошибки HTTP
        data = response.json()
        json_logger.info(f"Получены цены акций: {data}")
        return data
    except requests.RequestException as e:
        json_logger.error(f"Ошибка при получении цен акций: {e}")
        return {}


def get_greeting(date_str):
    """
    Принимает строку 'YYYY-MM-DD HH:MM:SS',
    возвращает приветствие по времени суток.
    """
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    hour = dt.hour

    if 5 <= hour < 12:
        greeting = "Доброе утро!"
    elif 12 <= hour < 18:
        greeting = "Добрый день!"
    elif 18 <= hour < 23:
        greeting = "Добрый вечер!"
    else:
        greeting = "Доброй ночи!"

    json_logger.info(f"Приветствие для {date_str}: {greeting}")
    return greeting


def process_cards(df):
    """
    Обработка данных по картам:
    - последние 4 цифры
    - общая сумма расходов
    - кешбэк (1 рубль на каждые 100 рублей)
    """
    cards = {}
    for _, row in df.iterrows():
        card_number = str(row["Номер карты"]).replace("*", "").strip()
        amount = float(row["Сумма платежа"])
        if card_number not in cards:
            cards[card_number] = 0
        cards[card_number] += abs(amount)

    result = []
    for last, total in cards.items():
        card_info = {"last_digits": last, "total_spent": round(total, 2), "cashback": round(total / 100, 2)}
        json_logger.info(
            f"Карта {card_info['last_digits']}: сумма={card_info['total_spent']}, кешбэк={card_info['cashback']}"
        )
        result.append(card_info)

    json_logger.info(f"Обработано карт: {len(result)}")
    return result


def get_top_transactions(df):
    """Возвращает топ-5 транзакций по сумме платежа."""
    df_sorted = df.sort_values(by="Сумма платежа", ascending=False).head(5)
    top = []
    for _, row in df_sorted.iterrows():
        transaction = {
            "date": row["Дата операции"],
            "amount": float(row["Сумма платежа"]),
            "category": row["Категория"],
            "description": row["Описание"],
        }
        top.append(transaction)
        json_logger.info(f"Топ-транзакция: {transaction}")
    json_logger.info(f"Количество топ-транзакций: {len(top)}")
    return top

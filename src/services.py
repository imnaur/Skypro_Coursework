import json
import logging
import os

import pandas as pd

# Логер для функции profitable_categories()
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_folder = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(log_folder, exist_ok=True)

LOG_FILE = os.path.join(log_folder, "services.log")

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


def profitable_categories(data: pd.DataFrame, year: int, month: int) -> dict:
    """Функция анализирует выгодные категории кэшбэков и возвращает их сумму."""
    json_logger.info(f"Запуск анализа кэшбэка за {month}/{year}")
    data["Дата операции"] = pd.to_datetime(data["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce")
    df_filtered = data[
        data["Дата операции"].apply(lambda x: x.year == year and x.month == month if pd.notnull(x) else False)
    ]
    json_logger.info(f"Количество транзакций после фильтрации: {len(df_filtered)}")

    if df_filtered.empty:
        return json.dumps({})

    df_filtered = df_filtered[["Категория", "Кэшбэк"]]
    df_filtered["Кэшбэк"] = pd.to_numeric(df_filtered["Кэшбэк"])

    grouped = df_filtered.groupby("Категория")["Кэшбэк"].sum()

    result = {cat: round(amount, 2) for cat, amount in grouped.items() if amount > 0}
    json_logger.info(f"Категории с кешбэком: {list(result.keys())}")
    return json.dumps(result, ensure_ascii=False)


if __name__ == "__main__":
    from pathlib import Path

    data_path = Path(__file__).parent.parent / "data" / "operations.xlsx"
    df = pd.read_excel(data_path, engine="openpyxl")
    report_json = profitable_categories(df, 2020, 12)
    print(report_json)

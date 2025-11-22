import json
import logging
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Optional

import pandas as pd

# Папка для отчётов
REPORTS_DIR = Path(__file__).parent.parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# Логирование
LOG_FILE = Path(__file__).parent.parent / "logs" / "reports.log"
logging.basicConfig(
    filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", encoding="utf-8"
)
logger = logging.getLogger(__name__)


def save_report(file_name: str = None):
    """Декоратор для сохранения отчетов."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Формируем имя файла по умолчанию, если не задано
            nonlocal file_name
            if not file_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{func.__name__}_{timestamp}.json"

            file_path = REPORTS_DIR / file_name

            # Сохраняем результат в файл
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)

            logger.info(f"Отчёт '{func.__name__}' сохранён в {file_path}")
            logger.debug(f"Содержимое отчёта: {result}")

            return result

        return wrapper

    if callable(file_name):
        func = file_name
        file_name = None
        return decorator(func)

    return decorator


@save_report
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Средние траты в рабочий и выходной день за последние 3 месяца."""
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%Y-%m-%d")

    three_months_ago = date - pd.DateOffset(months=3)

    # Преобразуем дату операции
    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
    )

    # Фильтруем последние 3 месяца
    df_filtered = transactions[transactions["Дата операции"] >= three_months_ago]
    logger.info(f"Фильтр транзакций за последние 3 месяца: {len(df_filtered)} строк")

    # Определяем рабочий или выходной день
    df_filtered["day_type"] = df_filtered["Дата операции"].dt.dayofweek.apply(
        lambda x: "workday" if x < 5 else "weekend"
    )

    # Средние траты по типу дня
    averages = df_filtered.groupby("day_type")["Сумма платежа"].mean().round(2)
    result = averages.to_dict()

    logger.info(f"Средние траты по типу дня: {result}")
    return result

from datetime import datetime

from src.reports import spending_by_workday
from src.services import profitable_categories
from src.utils import get_top_transactions, process_cards, read_excel


def run_all():
    # Чтение данных
    df = read_excel()

    print("=== Обработка карт ===")
    cards_report = process_cards(df)
    for card in cards_report:
        print(card)

    print("\n=== Топ-5 транзакций ===")
    top_transactions = get_top_transactions(df)
    for txn in top_transactions:
        print(txn)

    print("\n=== Средние траты по рабочим/выходным дням ===")
    spending_report = spending_by_workday(df)
    print(spending_report)

    print("\n=== Категории с кэшбэком ===")
    year = datetime.now().year
    month = datetime.now().month
    cashback_report = profitable_categories(df, year, month)
    print(cashback_report)


if __name__ == "__main__":
    run_all()
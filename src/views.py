from utils import (get_currency_rates, get_greeting, get_stock_prices, get_top_transactions, process_cards, read_excel,
                   read_user_settings)


def main(date_str):
    """Главная функция, отвечает за работоспособность и
    объединяет все функции."""
    # Приветствие
    greeting = get_greeting(date_str)

    # Чтение пользовательских настроек
    settings = read_user_settings()
    currencies = settings["user_currencies"]
    stocks = settings["user_stocks"]

    # Чтение файла
    df = read_excel()
    cards = process_cards(df)
    top_transactions = get_top_transactions(df)

    # Вызов доп. функций
    currency_raw = get_currency_rates(currencies)
    currency_rates = [{"currency": k.replace("USD", ""), "rate": v} for k, v in currency_raw["quotes"].items()]
    stock_raw = get_stock_prices(stocks)
    stock_prices = [{"stock": item["symbol"], "price": item["close"]} for item in stock_raw["data"]]

    # Финальный формат
    result = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
    return result


if __name__ == "__main__":
    print(main("2025-01-20 23:12:00"))

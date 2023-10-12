import time
import yfinance as yf
from db import cur


def view_stocks():
    while True:
        cur.execute("SELECT * FROM stocks")
        stocks = cur.fetchall()
        if not stocks:
            print("No stocks found.")
            time.sleep(1)
            break

        for index, stock in enumerate(stocks, 1):
            print(f"[{index}] {stock[1]}")
        print("[0] Back")
        print()
        choice = input(
            "Enter the number of a stock to view details or [0] to go back: "
        ).strip()

        if choice == "0":
            break

        try:
            choice = int(choice)
            if 1 <= choice <= len(stocks):
                stock = stocks[choice - 1]
                ticker = stock[1]
                stock_data = yf.Ticker(ticker)
                full_name = stock_data.info.get("longName", "N/A")
                current_price = stock_data.history(
                    period="1d")["Close"].iloc[0]
                current_cost = round(float(stock[3]) * current_price, 2)
                current_price = round(current_price, 2)
                total_cost = float(stock[5])
                difference = stock[8]

                menu_width = 70
                print("=" * menu_width)
                print(
                    f"""
                Ticker: {ticker},
                Full Name: {full_name},
                Shares: {stock[3]},
                Price per Share: {stock[4]},
                Current Price: {current_price},
                Total Cost: {total_cost},
                Current Cost: {current_cost},
                Difference: {difference}
"""
                )
                print("=" * menu_width)
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid option.")
        print()
        input("Press Enter to continue...")

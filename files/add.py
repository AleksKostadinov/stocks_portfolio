import time
import psycopg2
import yfinance as yf
from db import cur, conn


def add_stock():
    add_ticker = input("Add ticker: ").upper()

    # Check if the ticker exists in the database
    cur.execute("SELECT * FROM stocks WHERE ticker = %s", [add_ticker])
    existing_stock = cur.fetchone()

    if existing_stock:
        print(f"Adding more shares to the existing stock with ticker: {add_ticker}")

        # Get the existing data for the stock
        shares_bought = float(existing_stock[3])
        price_per_share = float(existing_stock[4])

        # Ask for the number of additional shares and the price per share
        additional_shares = float(
            input("Enter the number of additional shares: ")
        )
        additional_price_per_share = float(
            input("Enter the price per share for the new purchase: ")
        )

        # Calculate the new shares bought and the new average price per share
        new_shares_bought = shares_bought + additional_shares
        new_price_per_share = (
            (shares_bought * price_per_share)
            + (additional_shares * additional_price_per_share)
        ) / new_shares_bought

        # Update the database with the new values
        cur.execute(
            "UPDATE stocks SET shares_bought = %s, price_per_share = %s WHERE ticker = %s",
            (new_shares_bought, new_price_per_share, add_ticker),
        )

        # Calculate total cost, current cost, and difference
        cur.execute(
            "SELECT current_price FROM stocks WHERE ticker = %s", [add_ticker])
        current_price = cur.fetchone()[0]

        total_cost = new_shares_bought * new_price_per_share
        current_cost = new_shares_bought * float(current_price)
        difference = current_cost - total_cost

        cur.execute(
            "UPDATE stocks SET total_cost = %s, current_cost = %s, difference = %s WHERE ticker = %s",
            (total_cost, current_cost, difference, add_ticker),
        )

        conn.commit()
        print(f"Shares added to {add_ticker} successfully!")
        time.sleep(1)

    else:
        # If the ticker doesn't exist, add it as a new stock
        print(f"Ticker {add_ticker} does not exist. Adding as a new stock.")

        stock_data = yf.Ticker(add_ticker)
        full_name = stock_data.info.get("longName", "N/A")
        shares_bought = float(input("Enter shares bought: "))
        price_per_share = float(input("Enter price per share bought: "))
        total_cost = shares_bought * price_per_share
        current_price = stock_data.history(period="1d")["Close"].iloc[0]
        current_cost = shares_bought * current_price
        difference = current_cost - total_cost

        try:
            cur.execute(
                """
                INSERT INTO stocks (ticker, full_name, shares_bought, price_per_share, total_cost, current_price, current_cost, difference)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    add_ticker,
                    full_name,
                    shares_bought,
                    price_per_share,
                    total_cost,
                    current_price,
                    current_cost,
                    difference,
                ),
            )
            conn.commit()
            print(f"Ticker {add_ticker} added!")
        except psycopg2.DatabaseError:
            print("Ticker already exists!")

    time.sleep(1)


import time
from db import cur, conn


def edit_stock():
    edit_ticker = input(
        "Enter the ticker of the stock you want to edit: ").upper()

    # Check if the ticker exists in the database
    cur.execute("SELECT * FROM stocks WHERE ticker = %s", [edit_ticker])
    existing_stock = cur.fetchone()

    if not existing_stock:
        print("Ticker does not exist!")
        time.sleep(1)
        return

    print(f"Editing stock with ticker: {existing_stock[1]}")

    # Allow the user to select what to edit
    print("\nWhat would you like to edit?")
    print("[1] Shares Bought")
    print("[2] Price per Share")
    choice = input("Enter your choice: ")

    if choice == "1":
        new_shares_bought = float(input("Enter the new shares bought: "))
        cur.execute(
            "UPDATE stocks SET shares_bought = %s WHERE ticker = %s",
            (new_shares_bought, edit_ticker),
        )

    elif choice == "2":
        new_price_per_share = float(input("Enter the new price per share: "))
        cur.execute(
            "UPDATE stocks SET price_per_share = %s WHERE ticker = %s",
            (new_price_per_share, edit_ticker),
        )

    else:
        print("Invalid choice. Please try again.")
        return

    # Calculate and update the total cost, current cost, and difference
    cur.execute(
        "SELECT current_price FROM stocks WHERE ticker = %s", [edit_ticker])
    current_price = cur.fetchone()[0]

    cur.execute(
        "SELECT shares_bought, price_per_share FROM stocks WHERE ticker = %s",
        [edit_ticker],
    )
    shares_bought, price_per_share = cur.fetchone()

    total_cost = shares_bought * price_per_share
    current_cost = shares_bought * current_price
    difference = current_cost - total_cost

    cur.execute(
        "UPDATE stocks SET total_cost = %s, current_cost = %s, difference = %s WHERE ticker = %s",
        (total_cost, current_cost, difference, edit_ticker),
    )

    conn.commit()
    print("Stock updated successfully!")
    time.sleep(1)

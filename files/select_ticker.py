import time
from db import cur, conn


def select_stock():
    select_ticker = input("Select ticker: ").upper()
    cur.execute(
        """
        SELECT * FROM stocks
        WHERE ticker = %s
    """,
        [select_ticker],
    )
    selected_stocks = cur.fetchall()

    if not selected_stocks:
        print("Ticker does not exist!")
        time.sleep(1)
        return

    for stock in selected_stocks:
        menu_width = 70
        print("=" * menu_width)
        print(
            f"""
                Ticker: {stock[1]},
                Full Name: {stock[2]},
                Shares: {stock[3]},
                Price per Share: {stock[4]},
                Current Price: {stock[6]},
                Total Cost: {stock[5]},
                Current Cost: {stock[6] *  stock[3]},
                Difference: {stock[8]}
"""
        )
        print("=" * menu_width)
    conn.commit()
    input("Press Enter to continue...")

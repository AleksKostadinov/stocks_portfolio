import time
from db import cur, conn


def delete_stock():
    delete_ticker = input("Delete ticker: ").upper()

    # Check if the ticker exists in the database
    cur.execute("SELECT * FROM stocks WHERE ticker = %s", [delete_ticker])
    existing_stock = cur.fetchone()

    if not existing_stock:
        print("Ticker does not exist!")
        time.sleep(1)
        return

    print(f"Are you sure you want to delete the stock with ticker: {existing_stock[1]}?")
    confirmation = input("Type 'yes' to confirm, or any other key to cancel: ").strip().lower()

    if confirmation == "yes":
        cur.execute("DELETE FROM stocks WHERE ticker = %s", [delete_ticker])
        conn.commit()

        if cur.rowcount > 0:
            print("Ticker deleted successfully.")
        else:
            print("Failed to delete the stock.")

    else:
        print("Deletion canceled.")

    time.sleep(1)

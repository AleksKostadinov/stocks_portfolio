import time
from view import view_stocks
from add import add_stock
from select_ticker import select_stock
from edit import edit_stock
from delete import delete_stock
from db import conn, create_stocks_table


def main():
    create_stocks_table()
    again = True
    while again:
        menu_width = 30
        print("=" * menu_width)
        print("        Main Menu")
        print("=" * menu_width)
        print("[1] View stock")
        print("[2] Add stock")
        print("[3] Search by ticker")
        print("[4] Edit stock")
        print("[5] Delete stock")
        print("[0] Exit")
        print()
        print("=" * menu_width)
        selection = input("Enter your selection: ")
        print("=" * menu_width)

        if str(selection) == "1":
            view_stocks()
        elif str(selection) == "2":
            add_stock()
        elif str(selection) == "3":
            select_stock()
        elif str(selection) == "4":
            edit_stock()
        elif str(selection) == "5":
            delete_stock()
        elif str(selection) == "0":
            again = False
        else:
            print("Incorrect selection!")
        time.sleep(1)


main()
conn.close()

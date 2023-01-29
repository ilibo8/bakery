euro = chr(8364)
data_file = "Data/data.xlsx"
reports_file = "Reports/by_day.txt"
current_file = "Reports/current.txt"
recipes_file = "Data/recipes.txt"

options_main = """
    1. Supplies
    2. Goods
    3. Products
    4. Bakery
    5. SALES
    6. Reports

* to End the Day enter 0
"""

options_goods = """
    1. Increase stock of Goods
    2. Add new Goods
    3. Remove Goods

* to return to Main enter 0
"""

options_products = """
    1. Add new Product 
    2. Withdraw Product
    3. Change price of a Product
    4. Add recipe to Product

* to return to Main enter 0
"""

options_report = """
    1. Current
    2. For specific day
    3. Display all
    4. Monthly report

* to return to Main enter 0
      	"""

options_sales = """
    1. Add item
    2. Remove item
    3. Cancel order
    4. Print bill

* to return to Main enter 0
      	"""


def make_choice(number: int) -> int:
    print("Choose option.", end="")
    while True:
        try:
            while True:
                choice = int(input(" >>> "))
                if choice in range(number + 1):
                    return choice
                else:
                    print("Choose appropriate number.")
                    continue
        except ValueError:
            print("Typing error. Try again.")
            continue


def ask_for_positive_number() -> int:
    while True:
        try:
            while True:
                number = int(input(" >>> "))
                if number > 0:
                    return number
                else:
                    print("Choose positive number.")
                    continue
        except ValueError:
            print("Typing error. Try again.")
            continue


def ask_for_float() -> float:
    while True:
        try:
            while True:
                number = float(input(">>> "))
                if number > 0:
                    return number
                else:
                    print("Must be over 0.")
                    continue
        except ValueError:
            print("Typing error. Try again.")
            continue





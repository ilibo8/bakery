from functools import reduce
import itertools
import os
import json
import pandas as pd
from goods import Goods
from products import Products
from recipes import Recipes
from reports import Reports


euro = chr(8364)
data_file = "Data/data.xlsx"
recipes_file = "Data/recipes.xlsx"
reports_file = "Reports/by_day.txt"
current_file = "Reports/current.txt"

options_main = """
    1. Supplies
    2. Buy goods
    3. Bake a product
    4. Change price
    5. SALES
    6. Reports

* to End the Day enter 0
"""

options_report = """
    1. Current
    2. For specific day
    3. Display all
    4. Monthly report

* to go back to the main meny enter 0
      	"""

options_sales = """
    1. Add item
    2. Remove item
    3. Cancel order
    4. Print bill

* to go back to the main meny enter 0
      	"""


def make_choice(number: int) -> int:
    print("Choose an option.", end="")
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


def ask_for_price() -> float:
    while True:
        try:
            while True:
                number = float(input("New price >>> "))
                if number > 0:
                    return number
                else:
                    print("Must be over 0.")
                    continue
        except ValueError:
            print("Typing error. Try again.")
            continue


def stock_info() -> str:
    string = ""
    string += f"\n{'CURRENTLY ON STOCK:':^48}"
    string += "\n-----------------------------------------------"
    string += f'\n{"Goods:": <25}{"Products:": <25}'
    string += "\n-----------------------------------------------"
    for goods, products in itertools.zip_longest(Goods.info(), Products.info(), fillvalue=""):
        string += f'\n{goods: <25}{products: <25}'
    return string


def import_data() -> None:
    """Initialize Goods"""
    data = pd.read_excel(data_file, sheet_name="goods init")
    for index, row in data.iterrows():
        name = row['Name']
        quantity = row['Quantity']
        measure = row['Measure']
        Goods(name, quantity, measure)

    """Initialize Products"""
    data = pd.read_excel(data_file, sheet_name="product init")
    for index, row in data.iterrows():
        name = row['Product name']
        price = row['Price']
        quantity = row['Quantity']
        Products(name, price, quantity)

    """Initialize Recipes"""
    r_dict = {}
    df = pd.read_excel(recipes_file)
    convert = [v.dropna().to_dict() for k, v in df.iterrows()]
    for item in convert:
        key = item.pop("Recipe for")
        r_dict[key] = item
    for key, value in r_dict.items():
        Recipes(name=key, quantity=value)


def get_day() -> int:
    if not os.path.isfile(reports_file):
        return 1
    else:
        with open(reports_file) as f:
            lines = f.read().splitlines()
            lines.reverse()
            report_dict = json.loads(lines.pop(0))
            last_day = report_dict.get('day')
            return last_day + 1


def export_data() -> None:
    name_goods = []
    quantity_goods = []
    measure_goods = []
    for item in Goods.all_goods:
        name_goods.append(item.name)
        quantity_goods.append(item.get_quantity())
        measure_goods.append(item.measure)
    g_dict = {"Name": name_goods, 'Quantity': quantity_goods, 'Measure': measure_goods}

    name_products = []
    price_products = []
    stock_products = []
    for item in Products.all_products:
        name_products.append(item.name)
        price_products.append(item.get_price())
        stock_products.append(item.get_stock())
    p_dict = {"Product name": name_products, 'Price': price_products, 'Quantity': stock_products}

    g_columns = ['Name', 'Quantity', 'Measure']
    p_columns = ['Product name', 'Price', 'Quantity']

    df1 = pd.DataFrame(g_dict, columns=g_columns, index=None)
    df2 = pd.DataFrame(p_dict, columns=p_columns, index=None)
    with pd.ExcelWriter(data_file) as w:
        df1.to_excel(w, sheet_name="goods init", index=False)
        df2.to_excel(w, sheet_name="product init", index=False)


def start_new_day_in_bills() -> None:
    with open("Reports/bills.txt", "a") as f:
        f.write(f"\nDAY {report_today.day}\n")


def check_if_we_sold_everything(for_sale: dict) -> bool:
    for name in for_sale:
        if for_sale[name][0] != 0:
            return False
        else:
            continue
    return True


def set_cart_items(name: str, quantity: int) -> None:
    """ product = [quantity sold, price for one, total price] """
    if name not in cart.keys():
        cart[name] = [quantity,
                      Products.find_product_and_get_price(name),
                      Products.calculate_price_for_multiple_products(name, quantity)]
    else:
        cart[name][0] += quantity
        cart[name][2] = Products.calculate_price_for_multiple_products(name, cart[name][0])


def calculate_total_in_cart() -> float:
    total_sum = 0
    for key in cart.keys():
        total_sum += cart.get(key)[2]
    return total_sum


def remove_from_cart(name: str, number: int) -> None:
    for key in cart.keys():
        if key == name:
            cart.get(key)[0] -= number
            cart.get(key)[2] -= Products.calculate_price_for_multiple_products(name, number)


def cart_to_str() -> str:
    cart_str = ""
    for key in cart.keys():
        cart_str += f'{key:14} ({cart.get(key)[1]} {euro}) x {cart.get(key)[0]:<5}  {cart.get(key)[2]} {euro}\n'
    cart_str += f'TOTAL ________________________  {calculate_total_in_cart()} {euro}'
    return cart_str


def cart_view(header="--------- CART --------"):
    print(f'\n{header}')
    print(cart_to_str())


if __name__ == '__main__':
    import_data()
    day = get_day()
    report_today = Reports(number=day, sold_items={}, remaining_items={}, baked={}, changed_price={}, total_sum=0)
    start_new_day_in_bills()
    cart = {}
    counter = 1

    try:
        while True:
            print(options_main)
            choice = make_choice(number=6)

            match choice:
                case 1:
                    """Supplies"""
                    print(stock_info())

                case 2:
                    """Buy goods"""
                    for item in Goods.info():
                        print(item)
                    while True:
                        goods = input("\nWhat do you want to buy >>> ").lower()
                        if goods not in Goods.names_of_all:
                            print("Wrong input. Choose one of the items on stock.")
                            continue
                        else:
                            break
                    print("How much do you want?", end="")
                    number = ask_for_positive_number()
                    Goods.buy(name=goods, number=number)

                case 3:
                    """Bake a product"""
                    enough_to_bake_one = []
                    not_enough_for_one = []
                    for recipe in Recipes.all_recipes:
                        if Recipes.check_there_is_enough_ingredients(recipe, 1):
                            enough_to_bake_one.append(recipe.name)
                        else:
                            not_enough_for_one.append(recipe.name)
                    if len(enough_to_bake_one) == 0:
                        print("Can't bake anything, you're out of stock.")
                    else:
                        print(f"\nYou can bake: {enough_to_bake_one}")
                        if len(not_enough_for_one) > 0:
                            print(f"To bake: {not_enough_for_one} you need to buy some goods.")
                        if len(Goods.check_for_low_stock()) > 0:
                            [print(f"{good.capitalize()} is low on stock.") for good in Goods.check_for_low_stock()]
                        while True:
                            product_name = input("What do you want to bake >>> ").lower()
                            if product_name not in enough_to_bake_one:
                                print("Wrong input.")
                                continue
                            else:
                                break
                        recipe = Recipes.find_recipe(product_name)
                        recipe.print_recipe()
                        bake_max = recipe.calculate_max_products_to_bake_based_on_stock()
                        print(f"\nMaximum you can bake is {bake_max}")
                        print("How much do you want to bake?", end="")
                        number = ask_for_positive_number()
                        Products.bake(name=product_name, number=number)
                        if number <= bake_max:
                            report_today.update_baked(product_name, number)

                case 4:
                    """Change price"""
                    print("Change price of which product ?")
                    print(Products.names_of_all)
                    choice = input("Your choice >>> ").lower()
                    while choice not in Products.names_of_all:
                        choice = input("Typing error, try again >>>").lower()
                    product = Products.find_product_by_name(choice)
                    print(f"{product.name.capitalize()} - {product.get_price()} {euro}")
                    new_price = ask_for_price()
                    prices = [product.get_price()]
                    print(f"{product.name.capitalize()} - old price: {product.get_price()} {euro}")
                    product.set_price(new_price)
                    prices.append(new_price)
                    print(f"{product.name.capitalize()} - new price: {product.get_price()} {euro}")
                    report_today.changed_price[product.name] = prices

                case 5:
                    """SALES"""
                    for_sale = Products.products_for_sale()
                    while True:
                        print(options_sales)
                        choice = make_choice(number=4)

                        match choice:
                            case 1:
                                """Add item"""
                                if len(for_sale) == 0:
                                    print("No products for sale. Need to bake some.")
                                else:
                                    if check_if_we_sold_everything(for_sale):
                                        print("No more products for sale, need to bake some.")
                                    else:
                                        print("\nWe currently have:")
                                        print("-------------------------------")
                                        for name in for_sale:
                                            if for_sale[name][0] > 0:
                                                print(f"{name:15} {for_sale[name][0]} pc(s) - "
                                                      f"{for_sale[name][1]} {euro}")

                                        product_name = input("\nWhat would you like to buy? >>> ").lower()
                                        while product_name not in for_sale:
                                            product_name = input("We don't have that. Try again. >>>").lower()
                                        print("How much do you want?", end="")
                                        while True:
                                            quantity_choice = ask_for_positive_number()
                                            if quantity_choice > for_sale[product_name][0]:
                                                print(f"We cannot sell you that many. "
                                                      f"We have {for_sale[product_name][0]} for sale.")
                                                print("How much do you want?", end="")
                                            else:
                                                break
                                        set_cart_items(product_name, quantity_choice)
                                        for_sale.get(product_name)[0] -= quantity_choice
                                        cart_view()

                            case 2:
                                """Remove item"""
                                if len(cart) == 0:
                                    print("Your cart is empty.")
                                else:
                                    print(cart_to_str())
                                    print("")
                                    print("What do you want to remove from your cart?", end="")
                                    while True:
                                        product_remove = input(" >>> ").lower()
                                        if product_remove not in cart.keys():
                                            print("Typing error. Try again ")
                                        else:
                                            break
                                    print("How much do you want do remove?")
                                    while True:
                                        number = ask_for_positive_number()
                                        if number > cart.get(product_remove)[0]:
                                            print("You don't have that many in your cart. Try again", end="")
                                        else:
                                            break
                                    remove_from_cart(product_remove, number)
                                    for_sale.get(product_remove)[0] += number
                                    cart_view()

                            case 3:
                                """Cancel order"""
                                for key in cart.keys():
                                    for_sale.get(key)[0] += cart.get(key)[0]
                                cart.clear()
                                print("Cart is empty.")
                            case 4:
                                """Print bill"""
                                if len(cart) == 0:
                                    print("Cart is empty.")
                                else:
                                    with open("Reports/bills.txt", "a") as f:
                                        f.write(f"\nBill no.{counter}\n")
                                        f.write(cart_to_str())
                                        f.write("\n")

                                    counter += 1
                                    cart_view(header="=============== BILL ===============")
                                    print("Thank you for your purchase.")
                                    for key in cart.keys():
                                        Products.change_stock_of_specific_product(key, cart.get(key)[0])
                                    report_today.update_sales_and_total_sum(cart)
                                    with open(current_file, "w") as f:
                                        f.write(Reports.serialization(report_today))
                                    cart.clear()
                            case 0:
                                break

                case 6:
                    """Reports"""
                    while True:
                        print(options_report)
                        choice_report = make_choice(number=4)

                        match choice_report:
                            case 1:
                                """Current"""
                                if os.path.getsize(current_file) == 0:
                                    print("No transactions yet.")
                                else:
                                    Reports.display_current_report()

                            case 2:
                                """For specific day"""
                                if os.path.getsize(reports_file) == 0:
                                    print("This is first day. No reports yet.")
                                else:
                                    report_today.print_day_with_suffix()
                                    print("Number of day to see the report", end="")
                                    while True:
                                        day_number = ask_for_positive_number()
                                        if day_number <= report_today.day:
                                            break
                                        else:
                                            print("Wrong number, try again.", end="")
                                            continue
                                    if day_number == report_today.day:
                                        print("Go to Current report.")
                                    if day_number < report_today.day:
                                        reports = Reports.deserialize_reports_to_list()
                                        report = reports.pop(day_number - 1)
                                        print("\n")
                                        report.display_report()

                            case 3:
                                """Display all"""
                                report_today.print_day_with_suffix()
                                reports = Reports.deserialize_reports_to_list()
                                if len(reports) == 0:
                                    print("This is first day, no reports yet.")
                                else:
                                    for report in reports:
                                        report.display_report()

                            case 4:
                                """Monthly report"""
                                if os.path.getsize(reports_file) == 0:
                                    print("This is first day, no reports yet.")
                                else:
                                    print("\n")
                                    report_today.print_day_with_suffix()
                                    reports = Reports.deserialize_reports_to_list()
                                    monthly = reduce(lambda x, y: x + y, reports)
                                    print(f"\n===== REPORT FOR {monthly.day} DAYS =====")
                                    print(monthly.display_sold_items_and_total_sum())
                                    print("\n")
                                    print("------- Products sorted by sale --------")
                                    Reports.display_sold_items_sorted(monthly.sold_items)
                            case 0:
                                break

                case 0:
                    print("Closing the day...")
                    report_today.set_remaining(Products.make_product_dict_for_report())
                    with open(reports_file, "a") as f:
                        f.write(f'{Reports.serialization(report_today)}\n')
                    open(current_file, 'w').close()
                    export_data()
                    break
    except Exception as e:
        print(e)
        report_today.set_remaining(Products.make_product_dict_for_report())
        with open(reports_file, "a") as f:
            f.write(f'{Reports.serialization(report_today)}\n')
        open(current_file, 'w').close()
        export_data()

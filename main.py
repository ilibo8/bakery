from functools import reduce
import os
import json
import pandas as pd
from utility import *
from goods import Goods
from products import Products
from reports import Reports


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
        Products(name, price, quantity, recipe={})

    """Initialize Recipes"""
    all_recipes = Products.deserialize_recipes_from_file(recipes_file)
    for recipe in all_recipes:
        for key, value in recipe.items():
            product = Products.find_product_by_name(key)
            product.recipe = value


def get_day() -> int:
    if os.path.getsize(reports_file) == 0:
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
                    "Supplies"
                    print(Products.stock_info())

                case 2:
                    "Goods"
                    print(options_goods)
                    choice_goods = make_choice(number=3)

                    "Increase stock of goods"
                    if choice_goods == 1:
                        "Add more Goods"
                        keys = list(range(1, (len(Goods.all_goods) + 1)))
                        name_and_qty = Goods.info_tuples()
                        add_items_options = dict(zip(keys, name_and_qty))
                        print("\nWhat do you want to add?")
                        print("------------------------------")
                        for key, value in add_items_options.items():
                            print(f"{key:3}. {value[0].capitalize():12} {value[1]:4} {value[2]}")
                        print("\n* to return to Main enter 0\n")
                        product_choice = make_choice(len(add_items_options))
                        if product_choice == 0:
                            pass
                        else:
                            print(f"How much {add_items_options.get(product_choice)[0]} do you want to add? ", end="")
                            qty = ask_for_float()
                            Goods.buy(name=str(add_items_options.get(product_choice)[0]), number=qty)

                    "Add new goods"
                    if choice_goods == 2:
                        Goods.add_new()

                    "Remove Goods"
                    if choice_goods == 3:
                        pass

                case 3:
                    "Products"
                    print(options_products)
                    choice_products = make_choice(number=5)

                    "Add new Product"
                    if choice_products == 1:
                        try:
                            Products.create_new()
                        except Exception as e:
                            print(e)

                    "Withdraw Product"
                    if choice_products == 2:
                        try:
                            Products.delete()
                        except Exception as e:
                            print(e)

                    "Change price of a Product"
                    if choice_products == 3:
                        keys = list(range(1, (len(Products.all_products) + 1)))
                        name_and_price = Products.info_tuples()
                        change_price_options = dict(zip(keys, name_and_price))
                        print("\nChange price of which product?")
                        print("-------------------------------")
                        for key, value in change_price_options.items():
                            print(f"{key:3}. {value[0].capitalize():12} {value[1]:4} {euro}")
                        print("\n* to return to Main enter 0\n")
                        product_choice = make_choice(len(change_price_options))
                        if product_choice == 0:
                            pass
                        else:
                            product_name = change_price_options.get(product_choice)[0]
                            product = Products.find_product_by_name(product_name)
                            print(f"New price for {change_price_options.get(product_choice)[0]}", end="")
                            new_price = ask_for_float()
                            prices = [product.get_price()]
                            product.set_price(new_price)
                            prices.append(new_price)
                            print(f"{product.name.capitalize()} - New price: {product.get_price()} {euro}")
                            report_today.changed_price[product.name] = prices

                    """Add recipe to Product"""
                    if choice_products == 4:

                        product_to_add_recipe = []
                        for product in Products.all_products:
                            if len(product.recipe) == 0:
                                product_to_add_recipe.append(product)
                        if len(product_to_add_recipe) == 0:
                            print("There are no products without recipes, first create one.")
                        else:
                            print("Products without recipes:")
                            numbers = list(range(1, (len(product_to_add_recipe) + 1)))
                            names = [product.name for product in product_to_add_recipe]
                            options = dict(zip(numbers, names))
                            print("Add recipe to which product?")
                            print("-------------------------------")
                            for key, value in options.items():
                                print(f"{key:3}. {value.capitalize():12}")
                            print("\n* to exit enter 0\n")
                            choice = make_choice(len(product_to_add_recipe))
                            if choice == 0:
                                print("Everything is canceled.")
                            else:
                                print(f'Add recipe for {options.get(choice)}.')
                                product = Products.find_product_by_name(options.get(choice))
                                product.recipe = Products.add_recipe_to_product()
                                print(f'{product.name.capitalize()} recipe: ', end="")
                                product.print_recipe()

                    """Change recipe of Product"""
                    if choice_products == 5:
                        pass

                case 4:
                    """Bakery"""
                    enough_to_bake_one = []
                    not_enough_for_one = []
                    for product in Products.all_products:
                        if product.check_there_is_enough_ingredients(1):
                            enough_to_bake_one.append(product.name)
                        else:
                            not_enough_for_one.append(product.name)
                    if len(enough_to_bake_one) == 0:
                        print("Can't bake anything now. Check stock of goods.")
                    else:
                        keys = list(range(1, (len(enough_to_bake_one) + 1)))
                        bake_options = dict(zip(keys, enough_to_bake_one))
                        if len(not_enough_for_one) > 0:
                            not_enough_for_one_str = ""
                            for item in not_enough_for_one:
                                not_enough_for_one_str += f"{item}, "
                            print(f"To bake: {not_enough_for_one_str[:-2]} you need to Increase stock of goods.")
                        if len(Goods.check_for_low_stock()) > 0:
                            [print(f"{good.capitalize()} is low on stock.") for good in Goods.check_for_low_stock()]
                        print("\nWhat do you want to bake?")
                        print("------------------------------")
                        for key, value in bake_options.items():
                            print(f"{key}. {value.capitalize()}")
                        print("\n* to return to Main enter 0\n")
                        number = make_choice(len(bake_options))
                        if number == 0:
                            pass
                        else:
                            product_name = bake_options.get(number)
                            product = Products.find_product_by_name(product_name)
                            print("For one : ", end="")
                            product.print_recipe()
                            bake_max = product.calculate_max_products_to_bake_based_on_stock()
                            print(f"\nMaximum to bake is {bake_max}")
                            print("How much do you want to bake?", end="")
                            number = ask_for_positive_number()
                            Products.bake(name=product_name, number=number)
                            if number <= bake_max:
                                report_today.update_baked(product_name, number)

                case 5:
                    "SALES"
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
                                if len(cart) == 0:
                                    print("Your cart is empty.")
                                else:
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
                    "Reports"
                    while True:
                        print(options_report)
                        choice_report = make_choice(number=4)

                        match choice_report:
                            case 1:
                                "Current"
                                if os.path.getsize(current_file) == 0:
                                    print("No transactions yet.")
                                else:
                                    Reports.display_current_report()

                            case 2:
                                "For specific day"
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
                                "Display all"
                                report_today.print_day_with_suffix()
                                reports = Reports.deserialize_reports_to_list()
                                if len(reports) == 0:
                                    print("This is first day, no reports yet.")
                                else:
                                    for report in reports:
                                        report.display_report()

                            case 4:
                                "Monthly report"
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
                    Products.serialize_recipes_to_file(recipes_file)
                    export_data()
                    break
    except Exception as e:
        print(e)
        report_today.set_remaining(Products.make_product_dict_for_report())
        with open(reports_file, "a") as f:
            f.write(f'{Reports.serialization(report_today)}\n')
        open(current_file, 'w').close()
        export_data()

import json
from goods import Goods
from project_exceptions import *
from utility import ask_for_float, make_choice, euro
from itertools import zip_longest


class Products:
    names_of_all = []
    all_products = []

    def __init__(self, name: str, price: float, on_stock: int, recipe: dict):
        self.name = name
        self.__price = price
        self.__on_stock = on_stock
        self.recipe = recipe
        Products.all_products.append(self)
        Products.names_of_all.append(self.name)

    def __str__(self):
        return f"{self.name} - {self.__on_stock} ({self.__price}{chr(8364)})"

    def get_stock(self) -> int:
        return self.__on_stock

    def get_price(self) -> float:
        return self.__price

    def set_price(self, new_price: float) -> None:
        self.__price = new_price

    def check_purchase_quantity(self, number: int) -> bool:
        """To use in cart while adding items for specific product."""
        if self.__on_stock < number:
            return False
        return True

    @classmethod
    def info(cls) -> list:
        return [product.__str__() for product in cls.all_products]

    @staticmethod
    def find_product_by_name(name: str) -> "Products":
        for product in Products.all_products:
            if product.name == name.lower():
                return product
        raise NotFound

    @classmethod
    def find_product_and_get_price(cls, name: str) -> float:
        product = Products.find_product_by_name(name)
        return product.get_price()

    @staticmethod
    def calculate_price_for_multiple_products(product_name: str, quantity: int) -> float:
        price = Products.find_product_and_get_price(product_name)
        return round(price * quantity, 2)

    @staticmethod
    def change_stock_of_specific_product(name: str, number: int) -> None:
        product = Products.find_product_by_name(name)
        product.__on_stock -= number

    @staticmethod
    def make_product_dict_for_report() -> dict:
        data = {}
        for product in Products.all_products:
            data[product.name] = [product.__on_stock, product.__price]
        return data

    @staticmethod
    def bake(name: str, number: int) -> None:
        try:
            product = Products.find_product_by_name(name)
            if product.check_there_is_enough_ingredients(number):
                product.change_goods_quantity_after_making_products(number)
                product = Products.find_product_by_name(name)
                product.__on_stock += number
            else:
                raise NotEnoughIngredients
        except Exception as e:
            print(e)
        else:
            print(f"Baked {number} {name}.")
            print(f"{product.name.capitalize()} is now - {product.__on_stock} on stock.")

    @classmethod
    def products_for_sale(cls) -> dict:
        """Filters the list of all products to offer only the ones available. To use in cart."""
        for_sale = {}
        for item in cls.all_products:
            if item.__on_stock > 0:
                for_sale[item.name] = [item.__on_stock, item.__price]
        return for_sale

    def print_recipe(self) -> None:
        for ingredient in self.recipe.keys():
            print(f"{ingredient} - {self.recipe[ingredient]}({Goods.get_measure_for_goods(ingredient)})", end=" ")

    def get_quantity_for_ingredient(self, ingredient_name: str) -> float:
        for ingredient, quantity in self.recipe.items():
            if ingredient == ingredient_name:
                return quantity
        raise NotFound

    def check_there_is_enough_ingredients(self, number_of_products_making: int) -> bool:
        if len(self.recipe) > 0:
            for name in self.recipe.keys():
                ingredient = Goods.find(name)
                quantity_after_making = ingredient.get_quantity() - \
                                        self.get_quantity_for_ingredient(ingredient.name) * number_of_products_making
                if quantity_after_making >= 0:
                    continue
                else:
                    return False
            return True

    def change_goods_quantity_after_making_products(self, number_of_products_making) -> None:
        for name in self.recipe.keys():
            ingredient = Goods.find(name)
            new_goods_quantity = ingredient.get_quantity() - \
                                 self.get_quantity_for_ingredient(ingredient.name) * number_of_products_making
            ingredient.set_quantity(new_goods_quantity)

    def calculate_max_products_to_bake_based_on_stock(self) -> int:
        numbers = []
        for name, value in self.recipe.items():
            good = Goods.find(name)
            numbers.append(int(good.get_quantity() // value))
        return min(numbers)

    @classmethod
    def info_tuples(cls) -> list:
        all_products = []
        for product in cls.all_products:
            name = product.name
            price = product.__price
            all_products.append((name, price))
        return all_products

    @classmethod
    def create_new(cls) -> None:
        string = "\nCurrent products:\n"
        for name in cls.names_of_all:
            string += f"{name}, "
        print(string[:-2])
        print("\nEnter name of product you would like to add?")
        new_product_name = input("To exit enter 0 >>> ").lower()
        if new_product_name == 0:
            pass
        else:
            while new_product_name in cls.names_of_all:
                if new_product_name.isdigit():
                    raise Exception("Cannot be a number.")
                new_product_name = input("Input error. Already have that product, try another one. >>> ").lower()
            print("Enter price for new product? ", end="")
            price = ask_for_float()
            Products(name=new_product_name, price=price, on_stock=0, recipe={})
            print(f"New product - {new_product_name} {price} {euro}")

    @staticmethod
    def add_recipe_to_product() -> dict:
        goods_str = ""
        for name in Goods.names_of_all:
            goods_str += f"{name}, "
        goods_str = goods_str[:-2]
        print(f"These are all goods available as ingredients: {goods_str}")
        answer = input("Is new ingredient necessary? Y/N >>> ").lower()
        while answer not in ('y', 'n'):
            answer = input("Wrong input, try again - Y/N for new ingredient >>> ").lower()
        if answer == 'y':
            pass
        else:
            ingredients = Goods.names_of_all
            numbers = list(range(1, (len(ingredients) + 1)))
            name = ingredients
            options = dict(zip(numbers, name))
            ingredients_to_use = set()
            print("Which ingredients do you need?")
            for number, name in options.items():
                print(f"{number:3}. {name.capitalize():12}")
            print("To exit enter 0")
            print("---------------------------")
            while True:
                product_choice = make_choice(len(options))
                if product_choice == 0:
                    if len(ingredients_to_use) == 0:
                        print("You need at least one ingredient.")
                        pass
                    else:
                        break
                else:
                    ingredients_to_use.add(options.get(product_choice))
                    string = ""
                    for item in ingredients_to_use:
                        string += f"{item}, "
                    print(f"Ingredients to use: {string[:-2]}")

            recipe = {}
            for name in ingredients_to_use:
                print(f"Enter quantity for {name} ({Goods.find(name).measure}) ", end="")
                value = ask_for_float()
                recipe[name] = value
            return recipe
    @classmethod
    def delete(cls):
        keys = list(range(1, (len(cls.all_products) + 1)))
        values = [product.name for product in cls.all_products]
        options = dict(zip(keys, values))
        print("\nWhich product to remove?")
        print("------------------------------")
        for key, value in options.items():
            print(f"{key:3}. {value.capitalize():12}")
        print("\n* to return to Main enter 0\n")
        choice = make_choice(number=len(values))
        if choice == 0:
            pass
        else:
            answer = input(f"Are you sure you want to remove {options.get(choice)}? Y/N >>>").lower()
            while answer not in ("y", "n"):
                answer = input(f"Please confirm removal of {options.get(choice)}? Y/N >>>").lower()
            if answer == "n":
                print("Canceled.")
            else:
                for product in cls.all_products:
                    if product.name == options.get(choice):
                        del product

    @staticmethod
    def stock_info() -> str:
        string = ""
        string += f"\n{'CURRENTLY ON STOCK:':^48}"
        string += "\n-----------------------------------------------"
        string += f'\n{"Goods:": <25}{"Products:": <25}'
        string += "\n-----------------------------------------------"
        for goods, products in zip_longest(Goods.info(), Products.info(), fillvalue=""):
            string += f'\n{goods: <25}{products: <25}'
        string += "\n-----------------------------------------------"
        return string

    """Functions regarding recipes"""

    @staticmethod
    def serialize_recipes_to_file(file) -> None:
        all_recipes = []
        for product in Products.all_products:
            recipe = {product.name: product.recipe}
            all_recipes.append(recipe)

        with open(file, 'w') as f:
            for recipe in all_recipes:
                recipe_json = json.dumps(recipe, sort_keys=True)
                f.write(recipe_json)
                f.write("\n")

    @staticmethod
    def deserialize_recipes_from_file(file) -> list:
        with open(file, 'r') as f:
            recipes_list_json = f.read().splitlines()
            all_recipes = []
            for recipe in recipes_list_json:
                all_recipes.append(json.loads(recipe))
        return all_recipes

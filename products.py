from goods import Goods
from project_exceptions import *


class Products:
    names_of_all = []
    all_products = []

    def __init__(self, name: str, price: int, on_stock: int, recipe: dict):
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
        print("For one we need - ", end="")
        for ingredient in self.recipe.keys():
            print(f"{ingredient}: {self.recipe[ingredient]}({Goods.get_measure_for_goods(ingredient)})", end=" ")

    def get_quantity_for_ingredient(self, ingredient_name: str) -> float:
        for ingredient, quantity in self.recipe.items():
            if ingredient == ingredient_name:
                return quantity
        raise NotFound

    def check_there_is_enough_ingredients(self, number_of_products_making: int) -> bool:
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


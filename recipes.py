from project_exceptions import *
from goods import Goods


class Recipes:
    all_recipes = []
    names = []

    def __init__(self, name: str, quantity: dict):
        self.name = name
        self.quantity = quantity
        Recipes.all_recipes.append(self)
        Recipes.names.append(self.name)

    def print_recipe(self) -> None:
        print("For one we need ", end="")
        for ingredient in self.quantity.keys():
            print(f"{ingredient}: {self.quantity[ingredient]}({Goods.get_measure_for_goods(ingredient)})", end=" ")

    def get_quantity_for_ingredient(self, ingredient_name: str) -> float:
        for ingredient, quantity in self.quantity.items():
            if ingredient == ingredient_name:
                return quantity
        raise NotFound

    def check_there_is_enough_ingredients(self, number_of_products_making: int) -> bool:
        for name in self.quantity.keys():
            ingredient = Goods.find(name)
            quantity_after_making = ingredient.get_quantity() - \
                                    self.get_quantity_for_ingredient(ingredient.name) * number_of_products_making
            if quantity_after_making >= 0:
                continue
            else:
                return False
        return True

    def change_goods_quantity_after_making_products(self, number_of_products_making) -> None:
        for name in self.quantity.keys():
            ingredient = Goods.find(name)
            new_goods_quantity = ingredient.get_quantity() - \
                                 self.get_quantity_for_ingredient(ingredient.name) * number_of_products_making
            ingredient.set_quantity(new_goods_quantity)

    def calculate_max_products_to_bake_based_on_stock(self) -> int:
        numbers = []
        for name, value in self.quantity.items():
            good = Goods.find(name)
            numbers.append(int(good.get_quantity() // value))
        return min(numbers)

    @classmethod
    def find_recipe(cls, name: str) -> "Recipes":
        for recipe in cls.all_recipes:
            if recipe.name == name:
                return recipe
        raise NotFound(name)

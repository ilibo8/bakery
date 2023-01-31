import json
from utility import ask_for_float


class Goods:
    all_goods = []
    names_of_all = []

    def __init__(self, name: str, quantity: float, measure: str):
        self.name = name
        self.__quantity = quantity
        self.measure = measure
        Goods.all_goods.append(self)
        Goods.names_of_all.append(self.name)

    def __str__(self) -> str:
        return f"{self.name} - {self.__quantity:.2f} ({self.measure})"

    def get_quantity(self) -> float:
        return self.__quantity

    def set_quantity(self, quantity: float) -> None:
        self.__quantity = quantity

    @classmethod
    def get_measure_for_goods(cls, name: str) -> str:
        for item in cls.all_goods:
            if item.name == name:
                return item.measure

    @classmethod
    def check_for_low_stock(cls) -> list:
        """Depending on product, bar for low is manually set."""
        goods_low_stock = []
        with open("Data/bar_to_check_for_low_stock.txt") as f:
            bar_for_low_stock = json.loads(f.readline())

        for item in cls.all_goods:
            if item.__quantity < bar_for_low_stock.get(item.name):
                goods_low_stock.append(item.name)
        return goods_low_stock

    @classmethod
    def buy(cls, name: str, number: float) -> None:
        goods = Goods.find(name)
        new_quantity = round(goods.__quantity + number, 2)
        goods.set_quantity(new_quantity)
        print(f"{goods.name.capitalize()} is now - {goods.__quantity} on stock.")

    @classmethod
    def info_tuples(cls) -> list:
        all_goods = []
        for goods in cls.all_goods:
            name = goods.name
            qty = goods.__quantity
            measure = goods.measure
            all_goods.append((name, qty, measure))
        return all_goods

    @classmethod
    def info(cls) -> list:
        return [goods.__str__() for goods in cls.all_goods]

    @classmethod
    def find(cls, name: str) -> "Goods":
        for item in cls.all_goods:
            if item.name == name:
                return item

    @classmethod
    def add_new(cls):
        while True:
            name = input("What would you like to add? Enter name or exit to return. >>> ").lower()
            if name in Goods.names_of_all:
                print("Already exists in system.")
            elif name == 'exit':
                break
            else:
                measure = input("Choose measure - 'kg' or 'piece'? >>> ").lower()
                while measure not in ('kg', 'piece'):
                    measure = input("Typing error. Choose measure - 'kg' or 'piece'? >>> ").lower()
                print("Enter quantity for goods as starting number on stock ", end="")
                quantity = ask_for_float()
                print('For doing check-ups on stock, enter number for this item to create alert for low stock. '
                      'Alert if it goes lower than ', end="")
                low_bar = ask_for_float()
                with open("Data/bar_to_check_for_low_stock.txt") as r:
                    bar_for_low_stock = json.loads(r.readline())
                    bar_for_low_stock[name] = low_bar
                    with open("Data/bar_to_check_for_low_stock.txt", 'w') as w:
                        json_object = json.dumps(bar_for_low_stock)
                        w.write(json_object)
                new = Goods(name=name, quantity=quantity, measure=measure)
                print(f"Added to stock {new.__str__()}")
                break

    @classmethod
    def remove(cls, name: str) -> None:
        for index, item in enumerate(cls.all_goods):
            if item.name == name:
                del cls.all_goods[index]
        with open("Data/bar_to_check_for_low_stock.txt") as r:
            bar_for_low_stock = json.loads(r.readline())
            del bar_for_low_stock[name]
            with open("Data/bar_to_check_for_low_stock.txt", 'w') as w:
                json_object = json.dumps(bar_for_low_stock)
                w.write(json_object)

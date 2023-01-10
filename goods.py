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
        for item in cls.all_goods:
            if item.name == "flour":
                if item.__quantity < 1.5:
                    goods_low_stock.append(item.name)
            if item.name == "eggs":
                if item.__quantity < 3:
                    goods_low_stock.append(item.name)
            if item.name == "butter":
                if item.__quantity < 0.3:
                    goods_low_stock.append(item.name)
            if item.name == "cheese":
                if item.__quantity < 1:
                    goods_low_stock.append(item.name)
            if item.name == "chocolate":
                if item.__quantity < 0.3:
                    goods_low_stock.append(item.name)
            if item.name == "banana":
                if item.__quantity < 3:
                    goods_low_stock.append(item.name)
            if item.name == "apples":
                if item.__quantity < 3:
                    goods_low_stock.append(item.name)
        return goods_low_stock

    @classmethod
    def buy(cls, name: str, number: float) -> None:
        goods = Goods.find(name)
        new_quantity = round(goods.__quantity + number, 2)
        goods.set_quantity(new_quantity)
        print(f"{goods.name} is now - {goods.__quantity} on stock.")

    @classmethod
    def info(cls) -> list:
        return [goods.__str__() for goods in cls.all_goods]

    @classmethod
    def find(cls, name: str) -> "Goods":
        for item in cls.all_goods:
            if item.name == name:
                return item

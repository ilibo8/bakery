import json

euro = chr(8364)
reports_file = "Reports/by_day.txt"
current_file = "Reports/current.txt"


class Reports:

    def __init__(self, number: int, sold_items: dict, remaining_items: dict, baked: dict, changed_price: dict,
                 total_sum: float):
        self.day = number
        self.sold_items = sold_items
        self.remaining_items = remaining_items
        self.baked = baked
        self.changed_price = changed_price
        self.total_sum = total_sum

    def print_day_with_suffix(self):
        today = self.day
        if today == 1 or today // 10 == 1:
            print(f"Today is {today}st.")
        elif today == 2 or today // 10 == 2:
            print(f"Today is {today}nd.")
        elif today == 3 or today // 10 == 3:
            print(f"Today is {today}rd.")
        else:
            print(f"Today is {today}th.")

    def __add__(self, other: "Reports") -> "Reports":
        """We take day of other to know how many days we have added. Key[1] is price for one, that stays the same"""
        self.day = other.day
        for key in other.sold_items.keys():
            if key not in self.sold_items.keys():
                self.sold_items[key] = other.sold_items.get(key)
            else:
                self.sold_items[key][0] += other.sold_items.get(key)[0]
                self.sold_items[key][2] += other.sold_items.get(key)[2]
        self.total_sum += other.total_sum
        return self

    def set_remaining(self, data: dict) -> None:
        self.remaining_items = data

    def update_baked(self, name: str, quantity: int) -> None:
        if name not in self.baked:
            self.baked[name] = quantity
        else:
            self.baked[name] += quantity

    def update_sales_and_total_sum(self, bill: dict) -> None:
        """Every time bill is issued, report for the day is updated with articles sold and their total sum. """
        for product in bill.keys():
            if product not in self.sold_items:
                self.sold_items[product] = [bill.get(product)[0], bill.get(product)[1], bill.get(product)[2]]
                self.total_sum += bill.get(product)[2]
            else:
                self.sold_items[product][0] += bill.get(product)[0]
                self.sold_items[product][2] += bill.get(product)[2]
                self.total_sum += bill.get(product)[2]

    @staticmethod
    def display_current_report() -> None:
        with open(current_file) as f:
            report_json = f.readline()
            report = Reports.deserialization(report_json)
            print(report.display_sold_items_and_total_sum())

    def display_report(self):
        print(f"============== DAY no.{self.day} ===============")
        print(self.display_sold_items_and_total_sum())
        print(self.display_baked_and_remaining())
        if len(self.changed_price) > 0:
            print(self.display_changed_price())

    def display_baked_and_remaining(self) -> str:
        string = "\n"
        if len(self.baked) == 0:
            string += "Nothing baked today. \n"
        else:
            string += "----------- Baked today -----------\n"
            for key in self.baked.keys():
                string += f"{key:15} - {self.baked.get(key)} pc(s)\n"
        string += "\n---------- Products remaining ----------\n"
        for key in self.remaining_items.keys():
            string += f"{key:15} - {self.remaining_items.get(key)[0]:3} pc(s), " \
                      f"price: {self.remaining_items.get(key)[1]}{euro}\n"
        return string

    def display_changed_price(self) -> str:
        string = ""
        for key in self.changed_price.keys():
            string += (f"Changed price for {key} from {self.changed_price.get(key)[0]}{euro}"
                  f" to {self.changed_price.get(key)[1]}{euro}")
        return string

    def display_sold_items_and_total_sum(self) -> str:
        string = "\n------------- SOLD -------------"
        for key in self.sold_items.keys():
            string += f"\n{key:15}({self.sold_items.get(key)[1]:^5}{euro}) - " \
                      f"{self.sold_items.get(key)[0]:^3} ({self.sold_items.get(key)[2]}{euro})"
        string += f"\nEARNINGS_______________________{self.total_sum} {euro}"
        return string

    @staticmethod
    def display_sold_items_sorted(data: dict) -> None:
        """1 is to go to items, 0 is to go to number not to price 1"""
        sorted_data = sorted(data.items(), key=lambda x: x[1][0], reverse=True)
        for product in sorted_data:
            print(f"{product[0]:15} - {product[1][0]:3}")

    def serialization(self) -> str:
        return json.dumps(self.__dict__, sort_keys=True)

    @staticmethod
    def deserialization(string: str) -> "Reports":
        report_dict = json.loads(string)
        return Reports(number=report_dict['day'],
                       sold_items=report_dict['sold_items'],
                       remaining_items=report_dict['remaining_items'],
                       baked=report_dict['baked'],
                       changed_price=report_dict['changed_price'],
                       total_sum=report_dict['total_sum'])

    @staticmethod
    def deserialize_reports_to_list() -> list:
        with open(reports_file) as f:
            reports_json = f.read().splitlines()
            reports = [Reports.deserialization(x) for x in reports_json]
            return reports

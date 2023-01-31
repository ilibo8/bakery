class ProjectExceptions(Exception):
    def __init__(self, message):
        super().__init__(message)


class NotFound(ProjectExceptions):
    def __init__(self, name):
        super().__init__(f"Cannot find data for entry: {name}.")


class NotEnoughIngredients(ProjectExceptions):
    def __init__(self):
        super().__init__("There is not enough ingredients.")

from consolemenu import *
from consolemenu.items import *

import logging

logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class MyFunctionItem(FunctionItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def action(self):
        super().action()
        result = self.get_return()
        item_three = MenuItem(f"Result: {result}")
        m.append_item(item_three)


def add(number):
    return number + number


m = ConsoleMenu("Title")
item = MenuItem("Item one")
item_two = MenuItem("Item Two")
func = MyFunctionItem("add numbers", add, [5])

m.append_item(item)
m.append_item(item_two)
m.append_item(func)
logging.debug("starting up")

m.show()

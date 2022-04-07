from datetime import datetime, timedelta
from typing import List, Dict

MAX_TIME_FOR_PROCESSING_ORDER_IN_MINUTES = 20


def _get_required_material_for_item(item: str):
    burger_patties = 0
    bacon = 0
    lettuce = 0
    tomato = 0
    veggie_patties = 0
    if "B" in item:
        bacon = 1
    if "L" in item:
        lettuce = 1
    if "T" in item:
        tomato = 1
    if "V" in item:
        veggie_patties = 1
    else:
        burger_patties = 1
    return burger_patties, bacon, lettuce, tomato, veggie_patties


class Item:
    def __init__(self, restaurant_id: str, order_time: str, order_id: str, item: str):
        self.restaurant_id = restaurant_id
        self.order_time = datetime.strptime(order_time, "%Y-%m-%d %H:%M:%S")
        self.order_id = order_id
        self.item = item
        self.cooking_finished_time = None
        self.assembling_finished_time = None
        self.packaging_finished_time = None
        self.inventory_available = None
        self.required_burger_patties = None
        self.required_bacon = None
        self.required_lettuce = None
        self.required_tomato = None
        self.required_veggie_patties = None

    def set_cooking_finished_time(
        self, cooker_available_time: datetime, cooking_time: int
    ):
        if cooker_available_time >= self.order_time:
            self.cooking_finished_time = cooker_available_time + timedelta(
                minutes=cooking_time
            )
        else:
            self.cooking_finished_time = self.order_time + timedelta(
                minutes=cooking_time
            )

    def set_assembling_finished_time(
        self, assembler_available_time: datetime, assembling_time: int
    ):
        if assembler_available_time >= self.cooking_finished_time:
            self.assembling_finished_time = assembler_available_time + timedelta(
                minutes=assembling_time
            )
        else:
            self.assembling_finished_time = self.cooking_finished_time + timedelta(
                minutes=assembling_time
            )

    def set_packaging_finished_time(
        self, packager_available_time: datetime, packaging_time: int
    ):
        if packager_available_time >= self.assembling_finished_time:
            self.packaging_finished_time = packager_available_time + timedelta(
                minutes=packaging_time
            )
        else:
            self.packaging_finished_time = self.assembling_finished_time + timedelta(
                minutes=packaging_time
            )

    def get_inventory_available(
        self,
        available_burger_patties: int,
        available_bacon: int,
        available_lettuce: int,
        available_tomato: int,
        available_veggie_patties: int,
    ):
        (
            self.required_burger_patties,
            self.required_bacon,
            self.required_lettuce,
            self.required_tomato,
            self.required_veggie_patties,
        ) = _get_required_material_for_item(self.item)

        if (
            available_burger_patties - self.required_burger_patties < 0
            or available_bacon - self.required_bacon < 0
            or available_lettuce - self.required_lettuce < 0
            or available_tomato - self.required_tomato < 0
            or available_veggie_patties - self.required_veggie_patties < 0
        ):
            self.inventory_available = False
        else:
            self.inventory_available = True
        return self.inventory_available


def _flat_orders(orders: List[Dict]) -> List[Item]:
    items_in_all_orders = []
    for order in orders:
        for item in order["items"]:
            items_in_all_orders.append(
                Item(
                    restaurant_id=order["restaurant_id"],
                    order_time=order["time"],
                    order_id=order["order_id"],
                    item=item,
                )
            )
    return items_in_all_orders


class Order:
    def __init__(
        self, restaurant_id: str, order_time: str, order_id: str, items: List[str]
    ):
        self.restaurant_id = restaurant_id
        self.order_time = datetime.strptime(order_time, "%Y-%m-%d %H:%M:%S")
        self.order_id = order_id
        self.items = items


class Restaurant:
    def __init__(
        self,
        restaurant_id: str,
        cooking_ability: int,
        cooking_time: int,
        assembling_ability: int,
        assembling_time: int,
        package_ability: int,
        packaging_time: int,
        burger_patties: int,
        lettuce: int,
        tomato: int,
        veggie_patties: int,
        bacon: int,
    ):
        self.restaurant_id = restaurant_id
        self.cooking_ability = cooking_ability
        self.cooking_time = cooking_time
        self.assembling_ability = assembling_ability
        self.assembling_time = assembling_time
        self.package_ability = package_ability
        self.packaging_time = packaging_time
        self.burger_patties = burger_patties
        self.lettuce = lettuce
        self.tomato = tomato
        self.veggie_patties = veggie_patties
        self.bacon = bacon
        self.processing_orders = []
        self.cookers = []
        self.assemblers = []
        self.packagers = []
        self.estimated_processed_items = []
        self.results = []

    def get_results(self):
        for item in self.estimated_processed_items:
            duration = (
                int(
                    (item.packaging_finished_time - item.order_time).total_seconds()
                    / 60
                )
                if item.packaging_finished_time is not None
                else None
            )
            index, order = next(
                (
                    (index, order)
                    for (index, order) in enumerate(self.results)
                    if order["order_id"] == item.order_id
                ),
                (None, None),
            )
            if order is None:
                self.results.append(
                    {
                        "restaurant_id": item.restaurant_id,
                        "order_id": item.order_id,
                        "inventory_available": item.inventory_available,
                        "duration": duration,
                    }
                )
            else:
                if order["inventory_available"] is True:
                    self.results[index]["duration"] = (
                        max(order["duration"], duration)
                        if duration is not None and order["duration"] is not None
                        else None
                    )

        results_in_strings = []
        for result in self.results:
            if (
                result["inventory_available"] is not True
                or result["duration"] > MAX_TIME_FOR_PROCESSING_ORDER_IN_MINUTES
            ):
                results_in_strings.append(
                    f'{result["restaurant_id"]},{result["order_id"]},REJECTED'
                )
            else:
                results_in_strings.append(
                    f'{result["restaurant_id"]},{result["order_id"]},ACCEPTED,{result["duration"]}'
                )
        return results_in_strings

    def process_orders(self, orders: List[Dict]):
        all_items = _flat_orders(orders)
        for item in all_items:
            self.process_item(item)
        while len(self.cookers) != 0:
            self.assemble(self.cookers[0])
            self.cookers.pop(0)
        while len(self.assemblers) != 0:
            self.package(self.assemblers[0])
            self.assemblers.pop(0)
        while len(self.packagers) != 0:
            self.estimated_processed_items.append(self.packagers[0])
            self.packagers.pop(0)
        for i in self.estimated_processed_items:
            print(
                i.item,
                i.order_id,
                i.cooking_finished_time,
                i.assembling_finished_time,
                i.packaging_finished_time,
            )

    def process_item(self, item: Item):
        inventory_available = item.get_inventory_available(
            available_burger_patties=self.burger_patties,
            available_bacon=self.bacon,
            available_lettuce=self.lettuce,
            available_tomato=self.tomato,
            available_veggie_patties=self.veggie_patties,
        )
        if inventory_available:
            self.burger_patties -= item.required_burger_patties
            self.lettuce -= item.required_lettuce
            self.tomato -= item.required_tomato
            self.veggie_patties -= item.required_veggie_patties
            self.bacon -= item.required_bacon
            self.cook(new_item=item)
        else:
            self.estimated_processed_items.append(item)

    def cook(self, new_item: Item):
        if len(self.cookers) < self.cooking_ability:
            new_item.set_cooking_finished_time(
                cooker_available_time=new_item.order_time,
                cooking_time=self.cooking_time,
            )
            self.cookers.append(new_item)
        else:
            self.move_cooked_item_to_assembling_and_add_new_item_to_process(new_item)

    def assemble(self, new_item: Item):
        if len(self.assemblers) < self.assembling_ability:
            new_item.set_assembling_finished_time(
                assembler_available_time=new_item.cooking_finished_time,
                assembling_time=self.assembling_time,
            )
            self.assemblers.append(new_item)
        else:
            self.move_assembled_item_to_packaging_and_add_new_item_to_process(new_item)

    def package(self, new_item: Item):
        if len(self.packagers) < self.package_ability:
            new_item.set_packaging_finished_time(
                packager_available_time=new_item.assembling_finished_time,
                packaging_time=self.packaging_time,
            )
            self.packagers.append(new_item)
        else:
            self.moved_packaged_item_to_finished_and_add_new_item_to_process(new_item)

    def move_cooked_item_to_assembling_and_add_new_item_to_process(
        self, new_item: Item
    ):
        new_item.set_cooking_finished_time(
            cooker_available_time=self.cookers[0].cooking_finished_time,
            cooking_time=self.cooking_time,
        )
        self.assemble(self.cookers[0])
        self.cookers.pop(0)
        self.cookers.append(new_item)

    def move_assembled_item_to_packaging_and_add_new_item_to_process(
        self, new_item: Item
    ):
        new_item.set_assembling_finished_time(
            assembler_available_time=self.assemblers[0].assembling_finished_time,
            assembling_time=self.assembling_time,
        )
        self.package(self.assemblers[0])
        self.assemblers.pop(0)
        self.assemblers.append(new_item)
        # self.cookers.pop(0)

    def moved_packaged_item_to_finished_and_add_new_item_to_process(
        self, new_item: Item
    ):

        new_item.set_packaging_finished_time(
            packager_available_time=self.packagers[0].packaging_finished_time,
            packaging_time=self.packaging_time,
        )
        self.estimated_processed_items.append(self.packagers[0])
        self.packagers.pop(0)
        self.packagers.append(new_item)

from typing import List, Dict
from functions.utils import flat_orders
from functions.item import Item

MAX_TIME_FOR_PROCESSING_ORDER_IN_MINUTES = 20


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
        self.cookers = []
        self.assemblers = []
        self.packagers = []
        self.estimated_processed_items = []
        self.results = []
        self.rejected_orders = []
        self.success = True
        self.inventory_original_state = [
            burger_patties,
            lettuce,
            tomato,
            veggie_patties,
            bacon,
        ]

    def reset(self):
        self.burger_patties = self.inventory_original_state[0]
        self.lettuce = self.inventory_original_state[1]
        self.tomato = self.inventory_original_state[2]
        self.veggie_patties = self.inventory_original_state[3]
        self.bacon = self.inventory_original_state[4]
        self.cookers = []
        self.assemblers = []
        self.packagers = []
        self.estimated_processed_items = []
        self.success = True

    def get_results(self):
        for item in self.estimated_processed_items:
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
                        "duration": item.duration,
                    }
                )
            else:
                self.results[index]["duration"] = max(order["duration"], item.duration)

        total_time = sum(order["duration"] for order in self.results)

        raw_results_in_strings = []
        for result in self.results:
            raw_results_in_strings.append(
                f'{result["restaurant_id"]},{result["order_id"]},ACCEPTED,{result["duration"]}'
            )
        for order_id in self.rejected_orders:
            raw_results_in_strings.append(f"{self.restaurant_id},{order_id},REJECTED")
        results_in_strings = sorted(
            raw_results_in_strings, key=lambda x: int(x.split(",")[1].replace("O", ""))
        )
        results_in_strings.append(f"{self.restaurant_id},TOTAL,{total_time}")
        results_in_strings.append(
            f"{self.restaurant_id},INVENTORY,{self.burger_patties},{self.lettuce},{self.tomato},{self.veggie_patties},{self.bacon}"
        )
        return results_in_strings

    def process_orders(self, orders: List[Dict]):
        all_items = flat_orders(orders)
        self._process_items(all_items)

    def _process_items(self, all_items: List[Item]):
        for item in all_items:
            success = self.process_item(item)
            if success is False:
                self.success = success
                break
        while len(self.cookers) != 0 and self.success:
            success = self.assemble(self.cookers[0])
            if success is False:
                self.success = success
                break
            self.cookers.pop(0)
        while len(self.assemblers) != 0 and self.success:
            success = self.package(self.assemblers[0])
            if success is False:
                self.success = success
                break
            self.assemblers.pop(0)
        while len(self.packagers) != 0 and self.success:
            duration = self.packagers[0].get_duration()
            if duration > MAX_TIME_FOR_PROCESSING_ORDER_IN_MINUTES:
                if self.packagers[0].order_id not in self.rejected_orders:
                    self.rejected_orders.append(self.packagers[0].order_id)
                self.success = False
                break
            self.estimated_processed_items.append(self.packagers[0])
            self.packagers.pop(0)
        if self.success is True:
            return
        else:
            filtered_items = [
                item for item in all_items if item.order_id not in self.rejected_orders
            ]
            self.reset()
            return self._process_items(filtered_items)

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
            return self.cook(new_item=item)
        else:
            if item.order_id not in self.rejected_orders:
                self.rejected_orders.append(item.order_id)
            return False

    def cook(self, new_item: Item):
        if len(self.cookers) < self.cooking_ability:
            new_item.set_cooking_finished_time(
                cooker_available_time=new_item.order_time,
                cooking_time=self.cooking_time,
            )
            self.cookers.append(new_item)
            return True
        else:
            return self.move_cooked_item_to_assembling_and_add_new_item_to_process(
                new_item
            )

    def assemble(self, new_item: Item):
        if len(self.assemblers) < self.assembling_ability:
            new_item.set_assembling_finished_time(
                assembler_available_time=new_item.cooking_finished_time,
                assembling_time=self.assembling_time,
            )
            self.assemblers.append(new_item)
            return True
        else:
            return self.move_assembled_item_to_packaging_and_add_new_item_to_process(
                new_item
            )

    def package(self, new_item: Item):
        if len(self.packagers) < self.package_ability:
            new_item.set_packaging_finished_time(
                packager_available_time=new_item.assembling_finished_time,
                packaging_time=self.packaging_time,
            )
            self.packagers.append(new_item)
            return True
        else:
            return self.moved_packaged_item_to_finished_and_add_new_item_to_process(
                new_item
            )

    def move_cooked_item_to_assembling_and_add_new_item_to_process(
        self, new_item: Item
    ):
        new_item.set_cooking_finished_time(
            cooker_available_time=self.cookers[0].cooking_finished_time,
            cooking_time=self.cooking_time,
        )
        success = self.assemble(self.cookers[0])
        self.cookers.pop(0)
        self.cookers.append(new_item)
        return success

    def move_assembled_item_to_packaging_and_add_new_item_to_process(
        self, new_item: Item
    ):
        new_item.set_assembling_finished_time(
            assembler_available_time=self.assemblers[0].assembling_finished_time,
            assembling_time=self.assembling_time,
        )
        success = self.package(self.assemblers[0])
        self.assemblers.pop(0)
        self.assemblers.append(new_item)
        return success

    def moved_packaged_item_to_finished_and_add_new_item_to_process(
        self, new_item: Item
    ):

        new_item.set_packaging_finished_time(
            packager_available_time=self.packagers[0].packaging_finished_time,
            packaging_time=self.packaging_time,
        )

        duration = self.packagers[0].get_duration()
        if duration > MAX_TIME_FOR_PROCESSING_ORDER_IN_MINUTES:
            if self.packagers[0].order_id not in self.rejected_orders:
                self.rejected_orders.append(self.packagers[0].order_id)
            return False
        else:
            self.estimated_processed_items.append(self.packagers[0])

        self.packagers.pop(0)
        self.packagers.append(new_item)
        return True

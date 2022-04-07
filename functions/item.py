from datetime import datetime, timedelta


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

from typing import Dict


def get_order(data: str) -> Dict:
    raw_data = data.strip().split(",")
    if len(raw_data) < 4:
        raise Exception(f"Input for order: {data} is invalid!")
    order = {
        "restaurant_id": raw_data[0],
        "time": raw_data[1],
        "order_id": raw_data[2],
        "items": raw_data[3:],
    }
    return order


def get_restaurant_capacity_and_inventory(data: str) -> Dict:
    raw_data = data.strip().split(",")
    if len(raw_data) != 12:
        raise Exception("Input for restaurant capacity and inventory is invalid!")
    restaurant_capacity_and_inventory = {
        "restaurant_id": raw_data[0],
        "cooking_ability": raw_data[1].replace("C", ""),
        "cooking_time": raw_data[2],
        "assembling_ability": raw_data[3].replace("A", ""),
        "assembling_time": raw_data[4],
        "package_ability": raw_data[5].replace("P", ""),
        "package_time": raw_data[6],
        "burger_patties": raw_data[7],
        "lettuce": raw_data[8],
        "tomato": raw_data[9],
        "veggie_patties": raw_data[10],
        "bacon": raw_data[11],
    }
    return restaurant_capacity_and_inventory


def handle_input_data(input_data: str) -> Dict:
    raw_data = input_data.strip().split("\n")
    processed_data = {
        "restaurant_capacity_and_inventory": get_restaurant_capacity_and_inventory(
            raw_data[0]
        ),
        "orders": [get_order(data) for data in raw_data[1:]],
    }
    return processed_data

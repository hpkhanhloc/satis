from typing import List, Dict
from functions.item import Item


def flat_orders(orders: List[Dict]) -> List[Item]:
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

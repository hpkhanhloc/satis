import pytest
from functions.utils import flat_orders
from functions.item import Item


@pytest.fixture(scope="function")
def test_flat_orders():
    orders = [
        {
            "restaurant_id": "R1",
            "time": "2020-12-08 19:15:31",
            "order_id": "O1",
            "items": ["BLT", "LT"],
        },
        {
            "restaurant_id": "R1",
            "time": "2020-12-08 19:15:32",
            "order_id": "O2",
            "items": ["VLT", "VT"],
        },
    ]
    result = flat_orders(orders)
    expected = [
        Item("R1", "2020-12-08 19:15:31", "O1", "BLT"),
        Item("R1", "2020-12-08 19:15:31", "O1", "LT"),
        Item("R1", "2020-12-08 19:15:32", "O2", "VLT"),
        Item("R1", "2020-12-08 19:15:32", "O2", "VT"),
    ]
    assert result == expected

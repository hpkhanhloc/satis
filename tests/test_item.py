from functions.item import Item
from datetime import datetime

mock_item = Item("R1", "2020-12-08 21:15:31", "O1", "BLT")


def test_set_cooking_finished_time():
    cooker_available_time = datetime.strptime(
        "2020-12-08 21:16:31", "%Y-%m-%d %H:%M:%S"
    )
    mock_item.set_cooking_finished_time(cooker_available_time, 1)
    expected = datetime.strptime("2020-12-08 21:17:31", "%Y-%m-%d %H:%M:%S")
    assert mock_item.cooking_finished_time == expected


def test_get_inventory_available():
    inventory_available = mock_item.get_inventory_available(200, 200, 100, 100, 100)
    assert inventory_available == True
    assert mock_item.required_bacon == 1
    assert mock_item.required_lettuce == 1
    assert mock_item.required_tomato == 1
    assert mock_item.required_burger_patties == 1
    assert mock_item.required_veggie_patties == 0

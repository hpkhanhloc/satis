from functions.handle_input_data import (
    get_order,
    get_restaurant_capacity_and_inventory,
    handle_input_data,
)
from fastapi.testclient import TestClient
from main import app
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

client = TestClient(app)


def test_get_order():
    data = "R1,2020-12-08 21:15:31,ORDER1,BLT,LT,VLT"
    result = get_order(data)
    expected = {
        "restaurant_id": "R1",
        "time": "2020-12-08 21:15:31",
        "order_id": "ORDER1",
        "items": ["BLT", "LT", "VLT"],
    }
    assert result == expected


def test_get_restaurant_capacity_and_inventory():
    data = "R1,4C,1,3A,2,2P,1,100,200,200,100,100"
    result = get_restaurant_capacity_and_inventory(data)
    expected = {
        "restaurant_id": "R1",
        "cooking_ability": "4",
        "cooking_time": "1",
        "assembling_ability": "3",
        "assembling_time": "2",
        "package_ability": "2",
        "package_time": "1",
        "burger_patties": "100",
        "lettuce": "200",
        "tomato": "200",
        "veggie_patties": "100",
        "bacon": "100",
    }
    assert result == expected


def test_handle_input_data():
    data = """R1,4C,1,3A,2,2P,1,100,200,200,100,100
    R1,2020-12-08 19:15:31,O1,BLT,LT,VLT
    R1,2020-12-08 19:15:32,O2,VLT,VT,BLT,LT,VLT"""
    result = handle_input_data(data)
    expected = {
        "restaurant_capacity_and_inventory": {
            "restaurant_id": "R1",
            "cooking_ability": "4",
            "cooking_time": "1",
            "assembling_ability": "3",
            "assembling_time": "2",
            "package_ability": "2",
            "package_time": "1",
            "burger_patties": "100",
            "lettuce": "200",
            "tomato": "200",
            "veggie_patties": "100",
            "bacon": "100",
        },
        "orders": [
            {
                "restaurant_id": "R1",
                "time": "2020-12-08 19:15:31",
                "order_id": "O1",
                "items": ["BLT", "LT", "VLT"],
            },
            {
                "restaurant_id": "R1",
                "time": "2020-12-08 19:15:32",
                "order_id": "O2",
                "items": ["VLT", "VT", "BLT", "LT", "VLT"],
            },
        ],
    }
    assert result == expected


def test_process_orders():
    body = {
        "input_data": "R1,4C,1,3A,2,2P,1,100,200,200,100,100\nR1,2020-12-08 19:15:31,O1,BLT,LT,VLT"
    }
    res = client.post("/orders", json=body)
    assert res.status_code == HTTP_200_OK
    assert res.json() == {
        "restaurant_capacity_and_inventory": {
            "restaurant_id": "R1",
            "cooking_ability": "4",
            "cooking_time": "1",
            "assembling_ability": "3",
            "assembling_time": "2",
            "package_ability": "2",
            "package_time": "1",
            "burger_patties": "100",
            "lettuce": "200",
            "tomato": "200",
            "veggie_patties": "100",
            "bacon": "100",
        },
        "orders": [
            {
                "items": ["BLT", "LT", "VLT"],
                "order_id": "O1",
                "restaurant_id": "R1",
                "time": "2020-12-08 19:15:31",
            }
        ],
    }


def test_process_orders_with_invalid_order():
    body = {
        "input_data": "R1,4C,1,3A,2,2P,1,100,200,200,100,100\nR1,2020-12-08 19:15:31,O1,BLT,LT,VLT\nR1,2020-12-08 19:15:32,O2"
    }
    res = client.post("/orders", json=body)
    assert res.status_code == HTTP_400_BAD_REQUEST
    assert res.json() == {
        "detail": "Input for order: R1,2020-12-08 19:15:32,O2 is invalid!"
    }


def test_process_orders_with_invalid_restaurant_capacity_and_inventory():
    body = {
        "input_data": "R1,4C,1,3A,2,2P,1,100,200,200\nR1,2020-12-08 19:15:31,O1,BLT,LT,VLT"
    }
    res = client.post("/orders", json=body)
    assert res.status_code == HTTP_400_BAD_REQUEST
    assert res.json() == {
        "detail": "Input for restaurant capacity and inventory is invalid!"
    }

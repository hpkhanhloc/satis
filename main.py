from typing import Optional, List

from fastapi import FastAPI
from functions.handle_input_data import handle_input_data
from functions.handle_orders import Restaurant, Order
from pydantic import BaseModel
from starlette.status import HTTP_200_OK

app = FastAPI()


class InputData(BaseModel):
    input_data: str


@app.post("/orders", status_code=HTTP_200_OK, response_model=List[str])
def process_orders(body: InputData):
    processed_data = handle_input_data(body.input_data)
    restaurant_capacity_and_inventory = processed_data[
        "restaurant_capacity_and_inventory"
    ]
    restaurant = Restaurant(
        restaurant_id=restaurant_capacity_and_inventory["restaurant_id"],
        cooking_ability=int(restaurant_capacity_and_inventory["cooking_ability"]),
        cooking_time=int(restaurant_capacity_and_inventory["cooking_time"]),
        assembling_ability=int(restaurant_capacity_and_inventory["assembling_ability"]),
        assembling_time=int(restaurant_capacity_and_inventory["assembling_time"]),
        package_ability=int(restaurant_capacity_and_inventory["package_ability"]),
        packaging_time=int(restaurant_capacity_and_inventory["package_time"]),
        burger_patties=int(restaurant_capacity_and_inventory["burger_patties"]),
        lettuce=int(restaurant_capacity_and_inventory["lettuce"]),
        tomato=int(restaurant_capacity_and_inventory["tomato"]),
        veggie_patties=int(restaurant_capacity_and_inventory["veggie_patties"]),
        bacon=int(restaurant_capacity_and_inventory["bacon"]),
    )
    restaurant.process_orders(orders=processed_data["orders"])
    results = restaurant.get_results()
    return results

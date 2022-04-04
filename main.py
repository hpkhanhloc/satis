from typing import Optional

from fastapi import FastAPI
from functions.order import handle_input_data
from pydantic import BaseModel

app = FastAPI()


class InputData(BaseModel):
    input_data: str


@app.post("/orders")
def process_orders(body: InputData):
    return handle_input_data(body.input_data)

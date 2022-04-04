from typing import Optional

from fastapi import FastAPI
from functions.handle_input_data import handle_input_data
from pydantic import BaseModel
from starlette.status import HTTP_200_OK

app = FastAPI()


class InputData(BaseModel):
    input_data: str


@app.post("/orders")
def process_orders(body: InputData, status_code=HTTP_200_OK):
    return handle_input_data(body.input_data)

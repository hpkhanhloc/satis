from fastapi.testclient import TestClient
from main import app
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

client = TestClient(app)


def test_process_one_order():
    body = {
        "input_data": "R1,4C,1,3A,2,2P,1,100,200,200,100,100\nR1,2020-12-08 19:15:31,O1,BLT,LT,VLT"
    }
    res = client.post("/orders", json=body)
    assert res.status_code == HTTP_200_OK
    assert res.json() == ["R1,O1,ACCEPTED,5"]


def test_process_multiple_orders():
    body = {
        "input_data": "R1,4C,1,3A,2,2P,1,100,200,200,100,100\nR1,2020-12-08 19:15:31,O1,BLT,LT,VLT\nR1,2020-12-08 19:15:32,O2,VLT,VT,BLT,LT,VLT\nR1,2020-12-08 19:16:05,O3,VLT,VT,BLT,LT,VLT"
    }
    res = client.post("/orders", json=body)
    assert res.status_code == HTTP_200_OK
    assert res.json() == ["R1,O1,ACCEPTED,5", "R1,O2,ACCEPTED,7", "R1,O3,ACCEPTED,11"]

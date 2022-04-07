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
    assert res.json() == [
        "R1,O1,ACCEPTED,5",
        "R1,TOTAL,5",
        "R1,INVENTORY,98,197,197,99,99",
    ]


def test_process_multiple_orders():
    body = {
        "input_data": "R1,4C,1,3A,2,2P,1,100,200,200,100,100\nR1,2020-12-08 19:15:31,O1,BLT,LT,VLT\nR1,2020-12-08 19:15:32,O2,VLT,VT,BLT,LT,VLT\nR1,2020-12-08 19:16:05,O3,VLT,VT,BLT,LT,VLT"
    }
    res = client.post("/orders", json=body)
    assert res.status_code == HTTP_200_OK
    assert res.json() == [
        "R1,O1,ACCEPTED,5",
        "R1,O2,ACCEPTED,7",
        "R1,O3,ACCEPTED,11",
        "R1,TOTAL,23",
        "R1,INVENTORY,94,189,187,93,97",
    ]


def test_process_multiple_orders_with_need_rejection():
    body = {
        "input_data": "R1,4C,1,3A,2,2P,1,100,200,200,100,100\nR1,2020-12-08 19:15:31,O1,BLT,LT,VLT\nR1,2020-12-08 19:15:32,O2,VLT,VT,BLT,LT,VLT\nR1,2020-12-08 19:16:05,O3,VLT,VT,BLT,LT,VLT\nR1,2020-12-08 19:17:15,O4,BT,BLT,VLT,BLT,BT,LT,VLT\nR1,2020-12-08 19:19:10,O5,BLT,LT,VLT\nR1,2020-12-08 19:15:32,O6,VLT,VT,BLT,VLT,BT\nR1,2020-12-08 19:16:05,O7,VLT,LT,BLT,LT,VLT\nR1,2020-12-08 19:17:15,O8,BT,BLT,VLT,BLT,BLT\nR1,2020-12-08 19:18:15,O9,BT,BLT,VLT,BLT,BLT\nR1,2020-12-08 19:21:10,O10,BLT,VLT\nR1,2020-12-08 19:25:17,O11,VT,VLT\nR1,2020-12-08 19:28:17,O12,VT,VLT"
    }
    res = client.post("/orders", json=body)
    assert res.status_code == HTTP_200_OK
    assert res.json() == [
        "R1,O1,ACCEPTED,5",
        "R1,O2,ACCEPTED,7",
        "R1,O3,ACCEPTED,11",
        "R1,O4,ACCEPTED,14",
        "R1,O5,ACCEPTED,14",
        "R1,O6,REJECTED",
        "R1,O7,REJECTED",
        "R1,O8,ACCEPTED,20",
        "R1,O9,REJECTED",
        "R1,O10,ACCEPTED,17",
        "R1,O11,ACCEPTED,14",
        "R1,O12,ACCEPTED,13",
        "R1,TOTAL,115",
        "R1,INVENTORY,82,173,166,84,87",
    ]

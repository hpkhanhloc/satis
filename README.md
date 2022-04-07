# Optimize ordering process

## Description

Code base for optimising the processing order of a burget joint.

The burger joint has different branches and each branch comes with different capacity for cooking, assembling, and packaging food along with the time it takes to process.

Each branch has an inventory to process burgers and usage of each material reduces inventory count by 1.

Each order must be process within `20 minutes or less`, `reject` if it can be processed within 20 minutes or the branch runs out of material.

### Order input

Each order comes as a new line with this format: `restaurant id,order time,order id,series of items separated by comma`

Example: `R1,2020-12-08 21:15:31,ORDER1,BLT,LT,VLT`

- Restaurant ID is R1
- Date and time of order is: 2020-12-08 21:15:31
- Order ID is ORDER1
- Order includes the following food to be cooked:
  - A burger with Bacon, Lettuce and Tomato
  - A burger with Lettuce and Tomato
  - A veggie burger with Lettuce and Tomato

### Branch capacity and invetory input

Each branch has different capacity for cooking, assembling and packaging also has inventory for burger, bacon, lettuce, tomato and veggie burger.

This information will be presented before any orders on the first lines of the input data.

Example: `R1,4C,1,3A,2,2P,1,100,200,200,100,100`

Restaurant with ID (R1) has the following structure:

- Restaurant ID
- Capacity for Cooking 4 burgers (including veggie)
- It takes 1 minute to cook each burger
- Capacity for Assembling 3 burgers
- It takes 2 minutes to assemble each burger
- Capacity to package 2 burgers
- It takes 1 minute to package each burger
- Has burger patties inventory for 100 orders
- Has lettuce inventory for 200 orders
- Has tomato inventory for 200 orders
- Has veggie patties inventory for 100 orders
- Has bacon inventory for 100 orders

### Output

Output should include:

- The ID of orders that can be processed along with the time it takes to process them and the ones being rejected because the branch is at full capacity.
- The total time it takes to process all orders for the branch.
- The state of inventory

Format:

```
<Restaurant ID>,<Order ID>,<Accepted or Rejected>,<expected processing time in minutes>
<Restaurant ID>,TOTAL,<Total time it takes to process all orders>
<Restaurant ID>,Inventory,<Patties inventory>,<Lettuce inventory>,<Tomato inventory>,<Veggie patties inventory>,<Bacon Inventory>
```

Example output for 3 orders:

```
R1,O1,ACCEPTED,8
R1,O2,ACCEPTED,7
R1,O3,REJECTED
R1,TOTAL,25
R1,INVENTORY,58,130,115,63,50
```

## Solution

This repository build a `FastAPI` backend which can receive input data via `POST` api and return the input in required format.

### Local setup and develop

- Clone this repository.
- Make sure installed `python` (this project uses python `3.9`).
- Install `Make`
- Install requirements by running: `make install-requirements`
- Run API locally by: `make run-api-locally`
- Run unit test: `make test`

### Using

#### Via `http://127.0.0.1:8000`

- Run API locally, by default setup it can be accessed via `http://127.0.0.1:8000`
- Send `POST` with json body:

```
{
    "input_data": "R1,4C,1,3A,2,2P,1,100,200,200,100,100\nR1,2020-12-08 19:15:31,O1,BLT,LT,VLT"
}
```

- And get result

#### Via FastAPI docs

- Run API locally, and access `http://127.0.0.1:8000/docs`
- Dropdown the api and click `Try it out`
- In request body field, input data as example:

```
{
  "input_data": "R1,4C,1,3A,2,2P,1,100,200,200,100,100\nR1,2020-12-08 19:15:31,O1,BLT,LT,VLT\nR1,2020-12-08 19:15:32,O2,VLT,VT,BLT,LT,VLT\nR1,2020-12-08 19:16:05,O3,VLT,VT,BLT,LT,VLT\nR1,2020-12-08 19:17:15,O4,BT,BLT,VLT,BLT,BT,LT,VLT\nR1,2020-12-08 19:19:10,O5,BLT,LT,VLT\nR1,2020-12-08 19:15:32,O6,VLT,VT,BLT,VLT,BT\nR1,2020-12-08 19:16:05,O7,VLT,LT,BLT,LT,VLT\nR1,2020-12-08 19:17:15,O8,BT,BLT,VLT,BLT,BLT\nR1,2020-12-08 19:18:15,O9,BT,BLT,VLT,BLT,BLT\nR1,2020-12-08 19:21:10,O10,BLT,VLT\nR1,2020-12-08 19:25:17,O11,VT,VLT\nR1,2020-12-08 19:28:17,O12,VT,VLT"
}
```

- Click `Execute` button, and get result

### Testing

The project covered some unit test, run by: `make test`

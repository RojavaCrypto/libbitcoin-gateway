import asyncio
import json
import sys
import websockets

async def test_fetch_last_height(websocket):
    print("Testing fetch last_height...")

    message = json.dumps({
        "command": "fetch_last_height",
        "id": 1,
        "params": [
        ]
    })
    print("Sending:", message)
    await websocket.send(message)

    response = json.loads(await websocket.recv())
    print(json.dumps(response, indent=2))

async def test_fetch_transaction(websocket):
    print("Testing fetch transaction...")

    message = json.dumps({
        "command": "fetch_transaction",
        "id": 1,
        "params": [
            "ee475443f1fbfff84ffba43ba092a70d291df233bd1428f3d09f7bd1a6054a1f"
        ]
    })
    print("Sending:", message)
    await websocket.send(message)

    response = json.loads(await websocket.recv())
    print(json.dumps(response, indent=2))

async def test_fetch_history(websocket):
    print("Testing fetch history...")

    message = json.dumps({
        "command": "fetch_history",
        "id": 1,
        "params": [
            "13ejSKUxLT9yByyr1bsLNseLbx9H9tNj2d"
        ]
    })
    print("Sending:", message)
    await websocket.send(message)

    response = json.loads(await websocket.recv())
    print(json.dumps(response, indent=2))

async def test_fetch_block_header(websocket):
    print("Testing fetch block_header...")

    message = json.dumps({
        "command": "fetch_block_header",
        "id": 1,
        "params": [
            "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
        ]
    })
    print("Sending:", message)
    await websocket.send(message)

    response = json.loads(await websocket.recv())
    print(json.dumps(response, indent=2))

async def test_fetch_block_transaction_hashes(websocket):
    print("Testing fetch block_transaction_hashes...")

    message = json.dumps({
        "command": "fetch_block_transaction_hashes",
        "id": 1,
        "params": [
            "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
        ]
    })
    print("Sending:", message)
    await websocket.send(message)

    response = json.loads(await websocket.recv())
    print(json.dumps(response, indent=2))

async def test_fetch_spend(websocket):
    print("Testing fetch spend...")

    message = json.dumps({
        "command": "fetch_spend",
        "id": 1,
        "params": [
            ("0530375a5bf4ea9a82494fcb5ef4a61076c2af807982076fa810851f4bc31c09",
             0)
        ]
    })
    print("Sending:", message)
    await websocket.send(message)

    response = json.loads(await websocket.recv())
    print(json.dumps(response, indent=2))

async def test_fetch_transaction_index(websocket):
    print("Testing fetch transaction_index...")

    message = json.dumps({
        "command": "fetch_transaction_index",
        "id": 1,
        "params": [
            "ee475443f1fbfff84ffba43ba092a70d291df233bd1428f3d09f7bd1a6054a1f"
        ]
    })
    print("Sending:", message)
    await websocket.send(message)

    response = json.loads(await websocket.recv())
    print(json.dumps(response, indent=2))

async def test_fetch_block_height(websocket):
    print("Testing fetch block_height...")

    message = json.dumps({
        "command": "fetch_block_height",
        "id": 1,
        "params": [
            "000000000000048b95347e83192f69cf0366076336c639f9b7228e9ba171342e"
        ]
    })
    print("Sending:", message)
    await websocket.send(message)

    response = json.loads(await websocket.recv())
    print(json.dumps(response, indent=2))

async def test_fetch_stealth(websocket):
    print("Testing fetch stealth...")

    message = json.dumps({
        "command": "fetch_stealth",
        "id": 1,
        "params": [
            "11", 419135
        ]
    })
    print("Sending:", message)
    await websocket.send(message)

    response = json.loads(await websocket.recv())
    print(json.dumps(response, indent=2))

async def test_ticker(websocket):
    print("Testing fetch stealth...")

    message = json.dumps({
        "command": "fetch_ticker",
        "id": 1,
        "params": [
            "USD"
        ]
    })
    print("Sending:", message)
    await websocket.send(message)

    response = json.loads(await websocket.recv())
    print(json.dumps(response, indent=2))

async def hello():
    async with websockets.connect('ws://localhost:8888') as websocket:
        #await test_fetch_last_height(websocket)
        #await test_fetch_transaction(websocket)
        #await test_fetch_history(websocket)
        #await test_fetch_block_header(websocket)
        #await test_fetch_block_transaction_hashes(websocket)
        #await test_fetch_spend(websocket)
        #await test_fetch_transaction_index(websocket)
        #await test_fetch_block_height(websocket)
        #await test_fetch_stealth(websocket)
        await test_ticker(websocket)

asyncio.get_event_loop().run_until_complete(hello())


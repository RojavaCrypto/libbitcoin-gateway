import asyncio
import json
import sys
import websockets

# python3 fake_broadcast.py
# python3 fake_txradar.py

async def test_broadcast(websocket):
    print("Testing broadcast...")

    # ee475443f1fbfff84ffba43ba092a70d291df233bd1428f3d09f7bd1a6054a1f
    message = json.dumps({
        "command": "broadcast_transaction",
        "id": 1,
        "params": [
            "010000000110ee96aa946338cfd0b2ed0603259cfe2f5458c32ee4bd7b88b583769c6b046e010000006b483045022100e5e4749d539a163039769f52e1ebc8e6f62e39387d61e1a305bd722116cded6c022014924b745dd02194fe6b5cb8ac88ee8e9a2aede89e680dcea6169ea696e24d52012102b4b754609b46b5d09644c2161f1767b72b93847ce8154d795f95d31031a08aa2ffffffff028098f34c010000001976a914a134408afa258a50ed7a1d9817f26b63cc9002cc88ac8028bb13010000001976a914fec5b1145596b35f59f8be1daf169f375942143388ac00000000"
        ]
    })
    print("Sending:", message)
    await websocket.send(message)

    while True:
        response = json.loads(await websocket.recv())
        print(json.dumps(response, indent=2))

async def hello():
    async with websockets.connect('ws://localhost:8888') as websocket:
        await test_broadcast(websocket)

asyncio.get_event_loop().run_until_complete(hello())


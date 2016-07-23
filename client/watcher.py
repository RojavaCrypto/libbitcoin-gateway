import asyncio
import json
import sys
import websockets

async def watch(websocket, address):
    print("Watching:", address)

    message = json.dumps({
        "command": "subscribe_address",
        "id": 1,
        "params": [
            address
        ]
    })
    print("Sending:", message)
    await websocket.send(message)

    while True:
        response = json.loads(await websocket.recv())
        print(json.dumps(response, indent=2))

async def hello():
    address = "15s5nojkHKxJz3GvpKD1S6DR9nKUxSzNko"
    address = "11"
    async with websockets.connect('ws://localhost:8888') as websocket:
        await watch(websocket, address)

asyncio.get_event_loop().run_until_complete(hello())


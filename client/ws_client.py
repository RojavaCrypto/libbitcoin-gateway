#!/usr/bin/env python

import asyncio
import websockets

import json

async def hello():
    async with websockets.connect('ws://localhost:8888') as websocket:

        message = json.dumps({
            "command": "fetch_last_height",
            "id": 1,
            "params": [
            ]
        })
        print("Sending:", message)

        await websocket.send(message)

        response = await websocket.recv()
        print(">", response)

asyncio.get_event_loop().run_until_complete(hello())


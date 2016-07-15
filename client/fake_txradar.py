#!/usr/bin/python3
import binascii
import random
import struct
import time
import zmq

tx_hash = "ee475443f1fbfff84ffba43ba092a70d291df233bd1428f3d09f7bd1a6054a1f"
tx_hash = bytes.fromhex(tx_hash)

context = zmq.Context()

server = context.socket(zmq.PUB)
server.bind("tcp://*:7678")

while True:
    ident = struct.pack("<I", random.randint(0, 1000))
    server.send_multipart((ident, tx_hash))
    time.sleep(0.5)


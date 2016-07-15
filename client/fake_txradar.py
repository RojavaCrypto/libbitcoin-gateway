#!/usr/bin/python3
import binascii
import random
import struct
import zmq

tx_hash = "0011"
tx_hash = bytes.fromhex(tx_hash)

context = zmq.Context()

server = context.socket(zmq.PUB)
server.bind("tcp://*:7678")

while True:
    ident = struct.pack("<I", random.randint(0, 1000))
    server.send_multipart((ident, tx_hash))


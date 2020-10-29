import time
import sys
import zmq

port = 5558

try:
    if sys.argv[1].isnumeric():
        port = sys.argv[1]


def test_listener():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect("tcp://127.0.0.1:" + port)
    while True:
        message = socket.recv()
        print( "Received:", message)

test_listener()

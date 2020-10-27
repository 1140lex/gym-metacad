import time
import zmq

def worker():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect("tcp://127.0.0.1:3000")
    while True:
        message = socket.recv()
        print( "Received:", message)

worker()

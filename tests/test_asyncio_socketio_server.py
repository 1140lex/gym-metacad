import socketio
import uvicorn
import json
from multiprocessing import Process, Pipe
# Server instantiation
sio = socketio.AsyncServer(async_mode = 'asgi', cors_allowed_origins='http://localhost:3000')

# Generic Python ASGI
app = socketio.ASGIApp(sio)

def events(app, sender):
    @sio.event
    async def connect(sid, environ):
        print('connect ', sid)

    @sio.event
    async def message(sid, data):
        sender.send(data)
        print('message ', data)

    @sio.event
    async def disconnect(sid):
        print('disconnect ', sid)

    uvicorn.run(app, host='0.0.0.0', port=3001)


if __name__ == '__main__':
    receiver, sender = Pipe(duplex=False)
    p = Process(target=events, args=(app, sender,))
    p.start()
    print("hello moto")
    while(True):
        print(receiver.recv())
        
    print("Timed Out")
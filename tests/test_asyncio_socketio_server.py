import socketio
import uvicorn
import multiprocessing
from multiprocessing import Process, Pipe
# Server instantiation
sio = socketio.AsyncServer(async_mode = 'asgi', cors_allowed_origins='http://localhost:3000')

# Generic Python ASGI
app = socketio.ASGIApp(sio)

def events(app):
    @sio.event
    async def connect(sid, environ):
        print('connect ', sid)

    @sio.event
    async def message(sid, data):
        print('message ', data)

    @sio.event
    async def disconnect(sid):
        print('disconnect ', sid)

    uvicorn.run(app, host='0.0.0.0', port=3001)


if __name__ == '__main__':
    p = Process(target=events, args=(app,))
    p.start()
import socketio
import asyncio
from aiohttp import web
# Server instantiation
sio = socketio.AsyncServer(async_mode = 'asgi', cors_allowed_origins='http://localhost:3000')

# Generic Python ASGI
app = web.Application()
sio.attach(app)

@sio.event
async def connect(sid, environ):
    print('connect ', sid)

@sio.event
async def message(sid, data):
    print('message ', data)

@sio.event
async def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=3001)

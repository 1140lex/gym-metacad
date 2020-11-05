import socketio
import eventlet
# Server instantiation
sio = socketio.Server(cors_allowed_origins='http://localhost:3000')

# Generic Python WSGI
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def message(sid, data):
    print('message ', data)
    #Message Logic goes here

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 3001)), app)
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 10:38:49 2021

@author: xseber
"""

import flask_socketio as fs
import flask as f


app = f.Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'covid'
socket = fs.SocketIO(app, cors_allowed_origins="*")
ROOM = 'room'

user_status = dict({})


@app.route('/')
def index():
    return f.render_template('index.html', room=ROOM)

@app.route('/<int:name>')
def log_w_id(name):
    f.session['name'] = name
    return f.render_template('index.html', room=ROOM)

@socket.event
def connect():
    print('Connected {}'.format(f.request.sid))
    fs.emit('ready', room=ROOM)
    user_status.update({f.session['name'] : f.request.sid})
    fs.join_room(room=ROOM, sid=f.request.sid)
    
@socket.event
def disconnect():
    fs.leave_room(room=ROOM, sid=f.request.sid)
    user_status.pop(f.session['name'])
    print('{} is disconnected'.format(f.request.sid))
    
@socket.event
def data(e):
    print('Message from {}: {}'.format(f.request.sid, e))
    fs.emit('data', e, room=ROOM, include_self=False)
    
if __name__ == '__main__':
    print('using gunicorn instead!!')
    socket.run(app,port= 8080)

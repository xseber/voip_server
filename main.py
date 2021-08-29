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


user_status = dict({})


@app.route('/')
def index():
    return f.render_template('index.html', room=f.session['room'])

@app.route('/<room>/<name>')
def log_w_id(name, room):
    f.session['name'] = name
    f.session['room'] = room
    return f.render_template('index.html', room=f.session['room'])

@socket.event
def connect():
    print('Connected {}'.format(f.request.sid))
    fs.emit('ready', room=f.session['room'])
    user_status.update({f.session['name'] : f.request.sid})
    fs.join_room(room=f.session['room'], sid=f.request.sid)
    
@socket.event
def disconnect():
    fs.leave_room(room=f.session['room'], sid=f.request.sid)
    user_status.pop(f.session['name'])
    print('{} is disconnected'.format(f.request.sid))
    
@socket.event
def data(e):
    print('Message from {}: {}'.format(f.request.sid, e))
    fs.emit('data', e, room=f.session['room'], include_self=False)
    
if __name__ == '__main__':
    print('using gunicorn instead!!')
    socket.run(app,port= 8080)

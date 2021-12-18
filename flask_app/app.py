from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from flask import Flask, render_template, session, redirect
from flask_mail import Mail
from functools import wraps
import pymongo
import uuid
import os
import flask_app.controllers as controllers

# APP + SOCKETIO
app = Flask(__name__)
app.secret_key = os.urandom(12)
socketio = SocketIO(app, cors_allowed_origins="*")

# CONTROLLERS
controllers.start(socketio)

# MAILING
mail = Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'tester@gmail.com'
app.config['MAIL_PASSWORD'] = 'testing'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# ACCESS TOKEN + CHECKING
with open('flask_app/config/access_token', 'r') as f:
  access_token = f.read()

@socketio.on('connect')
def connect(auth):
  if access_token != auth:
    return False
  session['current_user'] = False

#RUN FUNCTION
def run(debug=True):
  socketio.run(app, debug=debug)

if __name__ == '__main__':
  run()
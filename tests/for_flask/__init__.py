import sys, os
sys.path.append(os.getcwd())

import unittest
import threading
import pymongo
import socketio
from flask_app.config import mongodb_settings
from flask_app.app import run as run_app
import pdb
import time


#START SERVER
app = threading.Thread(target=run_app, args=(False,))
app.start()

#DB ACCESS
mongodb_settings = mongodb_settings.get()

server_uri = 'http://127.0.0.1:5000/'

client = pymongo.MongoClient(mongodb_settings['host'], mongodb_settings['port'])
db = client[mongodb_settings['database']]
user_db = db['users']
chat_db = db['chats']

def clear_db():
    user_db.delete_many({})
    chat_db.delete_many({})

clear_db()

# RESPONSE
class Response():
    response = None
    def set(self, response):
        self.response = response

    def get(self, wait_for=0.5):
        old = time.time()
        new = old
        while self.response is None:
            new = time.time()
            if (new-old) > wait_for:
                raise Exception('timeout')
        return self.response

# HELPERS

def get_connected_socketio(token='C960128C640F6A4980B2E5DE454457751649090A1611E782A022EB236C1FD79C'):
    sio_client = socketio.Client()
    
    try:
        sio_client.connect(server_uri, auth=token)
    except socketio.exceptions.ConnectionError:
        return None
        
    return sio_client

def get_from_sio(sio, event_name):
    response = Response()
    sio.on(event_name, response.set)

    return response

def emit_and_get(user_sio, event_name, data=None):
    response = get_from_sio(user_sio, event_name)
    if not data:
        user_sio.emit(event_name)
    else:
        user_sio.emit(event_name, data=data)

    return response.get()


import sys, os
sys.path.append(os.getcwd())

import unittest
import threading
import pymongo
import time
import socketio
from flask_app.config import mongodb_settings
from flask_app.app import run as run_app


#START SERVER
app = threading.Thread(target=run_app, args=(False,))
app.start()

#DB ACCESS
mongodb_settings = mongodb_settings.get()

server_uri = 'http://127.0.0.1:5000/'

client = pymongo.MongoClient(mongodb_settings['host'], mongodb_settings['port'])
db = client[mongodb_settings['database']]
user_db = db['users']
user_db.delete_many({})

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

def get_connected_socketio(token='8NEKRW6YXDJ2G4IZCHOR3WW0AU8V6GXJB6LEO5GIHXYNSV5GE7DVMZOTGMTE9NNO'):
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

def sign_up(sio, custom = {}):
    signup_dict = {  
                'email':'hikaridesuyoo@gmail.com',
                'username':'hikari',
                'password':'senha123',
                'password_confirm':'senha123'
            }

    signup_dict.update(custom)
    
    sio.emit('signup',
        signup_dict
        )

def full_signup(sio, confirm_email = True):
    response = get_from_sio(sio, 'signup')
    sign_up(sio)
    response.get()

    user = user_db.find_one({'email':'hikaridesuyoo@gmail.com'})

    if confirm_email:
        response = get_from_sio(sio, 'verify_email')
        sio.emit('verify_email', user['verification_code'])
        response.get()

    user = user_db.find_one({'email':'hikaridesuyoo@gmail.com'})

    return user



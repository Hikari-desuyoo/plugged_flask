from flask_app.controllers.controller import Controller
from flask import session

class ConnectionCheckerController(Controller):
    def on_ping(self):
        return 'pong'




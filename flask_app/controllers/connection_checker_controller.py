from flask_app.controllers.controller import Controller
from flask_app.models.user import User
from flask import session

class ConnectionCheckerController(Controller):
    def on_ping(self):
        return 'pong'




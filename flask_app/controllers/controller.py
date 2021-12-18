from flask_socketio import emit
from flask import session
import pymongo
from flask_app.models.user import User
from inspect import signature
import inspect
import pdb

class InbuiltController:   
    """
    Controller with basic functionality provided by the framework
    """

    endpoint_method_prefix = 'on_'
    def __init__(self, sio):
        self.sio = sio
        self.set_all_endpoints()
        self.further_initialize()

    def further_initialize(self):
        """Will be called right after initialize, and can be overwritten."""
        pass

    def set_all_endpoints(self):
        """Sends all endpoint methods(the ones starting with on_ ) to be processed by self.set_endpoint"""

        controller_list = inspect.getmembers(self, predicate=inspect.ismethod)

        for controller_tuple in controller_list:
            name, method = (controller_tuple[0], controller_tuple[1])
            if name.startswith(self.endpoint_method_prefix):
                self.set_endpoint(method)


    def set_endpoint(self, endpoint_method):
        """Applies the endpoint on the socket"""
        event_name = endpoint_method.__name__
        prefix_length = len(self.endpoint_method_prefix)
        event_name = event_name[prefix_length: len(event_name)]

        @self.sio.on(event_name)
        def event_method(data=None):
            if len(signature(endpoint_method).parameters) == 1:
                response_data = endpoint_method(data)
            else:
                response_data = endpoint_method()

            emit(event_name, response_data)

class Controller(InbuiltController):
    """
    Controller to be inherited by all other controllers. 
    If it's needed to create methods shared between controllers, do it here.
    """
    def get_current_user(self):
        return session.get('current_user', None)

    def is_current_user_email_verified(self): 
        current_user = self.get_current_user()
        return current_user and not current_user['verification_code']

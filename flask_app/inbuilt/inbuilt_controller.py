from flask_socketio import emit
from inspect import signature
import inspect

class InbuiltController:   
    """
    Controller with basic functionality provided by the framework
    """

    endpoint_method_prefix = 'on_'
    def __init__(self, sio):
        self.sio = sio
        self.before_action_dictionary = {}
        self.further_initialize()
        self.set_all_endpoints()

    def add_before_actions(self, new_before_actions):
        self.before_action_dictionary.update(new_before_actions)

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

        before_action = lambda : None
        
        for before_action_method, event_list in self.before_action_dictionary.items():
            if event_list == 'all' or (endpoint_method.__name__ in event_list):
                before_action = before_action_method
                continue


        @self.sio.on(event_name)
        def event_method(data=None):
            before_action_response = before_action()
            if before_action_response: 
                emit(event_name, before_action_response)
                return

            if len(signature(endpoint_method).parameters) == 1:
                response_data = endpoint_method(data)
            else:
                response_data = endpoint_method()

            emit(event_name, response_data)

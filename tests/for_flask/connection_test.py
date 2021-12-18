from . import *

class Connection(unittest.TestCase):
    def test_connection(self):
        sio = get_connected_socketio()

        response = get_from_sio(sio, 'ping')
        sio.emit('ping')
        
        self.assertNotEqual(sio, None)
        self.assertEqual(response.get(), 'pong')

    def test_connection_wrong_token(self):
        sio = get_connected_socketio('1')
        self.assertEqual(sio, None)
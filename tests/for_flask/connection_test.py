from . import *

class Connection(unittest.TestCase):
    def test_connection(self):
        sio = get_connected_socketio()

        response = emit_and_get(sio, 'ping')
        
        self.assertNotEqual(sio, None)
        self.assertEqual(response, 'pong')

    def test_connection_twice(self):
        sio = get_connected_socketio()
        sio2 = get_connected_socketio()

        response = emit_and_get(sio, 'ping')
        response2 = emit_and_get(sio2, 'ping')

        self.assertNotEqual(sio.get_sid(), sio2.get_sid())
        self.assertEqual(response, 'pong')
        self.assertEqual(response2, 'pong')

    def test_connection_wrong_token(self):
        sio = get_connected_socketio('1')
        self.assertEqual(sio, None)
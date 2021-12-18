from . import *

class GetUserInfo(unittest.TestCase):
    def test_success(self):
        sio = get_connected_socketio()
        user_db.delete_many({})

        current_user = full_signup(sio)
        response = get_from_sio(sio, 'get_user_info')
        sio.emit('get_user_info')

        user_info = response.get()
        del current_user['password']

        self.assertEqual(current_user, user_info)

    def test_no_email_confirmation(self):
        sio = get_connected_socketio()
        user_db.delete_many({})

        current_user = full_signup(sio, confirm_email=False)
        response = get_from_sio(sio, 'get_user_info')
        sio.emit('get_user_info')

        with self.assertRaises(Exception):
            response.get()

    def test_not_logged(self):
        sio = get_connected_socketio()
        user_db.delete_many({})

        response = get_from_sio(sio, 'get_user_info')
        sio.emit('get_user_info')

        with self.assertRaises(Exception):
            response.get()
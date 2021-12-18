from . import *


class Logout(unittest.TestCase):
    def test_logout_invalid(self):
        user_db.delete_many({})
        sio = get_connected_socketio()
        response = get_from_sio(sio, 'logout')
        sio.emit('logout')

        self.assertEqual(response.get(), 'not_logged')

    def test_logout_succesfully(self):
        user_db.delete_many({})
        sio = get_connected_socketio()
        response = get_from_sio(sio, 'signup')
        sign_up(sio)
        response.get()
        
        response = get_from_sio(sio, 'logout')
        
        sio.emit('logout')

        self.assertEqual(response.get(), 'success')
        self.assertFalse(user_db.find_one({'email':'hikaridesuyoo@gmail.com'})['online'])

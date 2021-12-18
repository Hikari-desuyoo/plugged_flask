from . import *

class VerifyEmail(unittest.TestCase):
    def test_success(self):
        user_db.delete_many({})
        sio = get_connected_socketio()

        response = get_from_sio(sio, 'signup')
        sign_up(sio)
        response.get()

        user = user_db.find_one({'email':'hikaridesuyoo@gmail.com'})
        
        response = get_from_sio(sio, 'verify_email')
        sio.emit('verify_email', user['verification_code'])

        self.assertEqual(response.get(), 'success')

    def test_fail(self):
        user_db.delete_many({})
        sio = get_connected_socketio()

        response = get_from_sio(sio, 'signup')
        sign_up(sio)
        response.get()

        user = user_db.find_one({'email':'hikaridesuyoo@gmail.com'})
        
        response = get_from_sio(sio, 'verify_email')
        sio.emit('verify_email', user['verification_code']+'2')

        self.assertEqual(response.get(), 'failed')

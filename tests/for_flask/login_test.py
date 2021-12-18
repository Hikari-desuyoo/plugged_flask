from . import *


class Login(unittest.TestCase):
    def test_login_success_email(self):
        user_db.delete_many({})
        sio = get_connected_socketio()

        response = get_from_sio(sio, 'signup')
        sign_up(sio)
        response.get()

        response = get_from_sio(sio, 'logout')
        sio.emit('logout')
        response.get()

        self.assertFalse(user_db.find_one({'email':'hikaridesuyoo@gmail.com'})['online'])

        response = get_from_sio(sio, 'login')
        sio.emit('login', 
        {
            'email': 'hikaridesuyoo@gmail.com',
            'password':'senha123'
        }
        )

        response.get()

        user = user_db.find_one({'email':'hikaridesuyoo@gmail.com'})

        self.assertEqual(response.get(), 'success')
        self.assertTrue(user_db.find_one({'email':'hikaridesuyoo@gmail.com'})['online'])

    def test_login_wrong_password(self):
        user_db.delete_many({})
        sio = get_connected_socketio()

        response = get_from_sio(sio, 'signup')
        sign_up(sio)
        response.get()

        response = get_from_sio(sio, 'logout')
        sio.emit('logout')
        response.get()

        self.assertFalse(user_db.find_one({'email':'hikaridesuyoo@gmail.com'})['online'])

        response = get_from_sio(sio, 'login')
        sio.emit('login', 
        {
            'email': 'hikaridesuyoo@gmail.com',
            'password':'senha123wrong'
        }
        )

        response.get()

        user = user_db.find_one({'email':'hikaridesuyoo@gmail.com'})

        self.assertEqual(response.get(), 'failed')
        self.assertFalse(user_db.find_one({'email':'hikaridesuyoo@gmail.com'})['online'])

    def test_login_wrong_email(self):
        user_db.delete_many({})
        sio = get_connected_socketio()

        response = get_from_sio(sio, 'signup')
        sign_up(sio)
        response.get()

        response = get_from_sio(sio, 'logout')
        sio.emit('logout')
        response.get()

        self.assertFalse(user_db.find_one({'email':'hikaridesuyoo@gmail.com'})['online'])

        response = get_from_sio(sio, 'login')
        sio.emit('login', 
        {
            'email': 'hikaridesuyoo@gmail.comwrong',
            'password':'senha123'
        }
        )

        response.get()

        user = user_db.find_one({'email':'hikaridesuyoo@gmail.com'})

        self.assertEqual(response.get(), 'failed')
        self.assertFalse(user_db.find_one({'email':'hikaridesuyoo@gmail.com'})['online'])

if __name__ == '__main__':
    unittest.main()
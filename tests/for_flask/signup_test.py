from . import *

class Signup(unittest.TestCase):
    def test_signup_successfully(self):
        user_db.delete_many({})
        sio = get_connected_socketio()
        response = get_from_sio(sio, 'signup')
        sign_up(sio)
        
        self.assertEqual(response.get(), 'success')
        user = user_db.find_one({'email':'hikaridesuyoo@gmail.com'})
        
        self.assertTrue(user)
        self.assertTrue(user['online'])
        
    def test_signup_bad_password(self):
        user_db.delete_many({})
        sio = get_connected_socketio()
        response = get_from_sio(sio, 'signup')
        sign_up(sio, custom={'password':'a', 'password_confirm':'a'})
        
        self.assertEqual(response.get(), ['bad_password'])
    
    def test_signup_repeated_email(self):
        user_db.delete_many({})
        sio = get_connected_socketio()
        response = get_from_sio(sio, 'signup')
        sign_up(sio, {'username':'aaaa'})
        response.get()

        sio = get_connected_socketio()
        response = get_from_sio(sio, 'signup')
        sign_up(sio)
        
        self.assertEqual(response.get(), ['email_in_use'])
        self.assertTrue(user_db.find_one({'email':'hikaridesuyoo@gmail.com'}))
    
    def test_signup_repeated_username(self):
        user_db.delete_many({})
        sio = get_connected_socketio()
        response = get_from_sio(sio, 'signup')
        sign_up(sio)
        response.get()

        sio = get_connected_socketio()
        response = get_from_sio(sio, 'signup')
        sign_up(sio, {'email':'aaaa@gm.com'})
        
        self.assertEqual(response.get(), ['username_in_use'])
        self.assertTrue(user_db.find_one({'email':'hikaridesuyoo@gmail.com'}))
    
    def test_signup_different_passwords(self):
        user_db.delete_many({})
        sio = get_connected_socketio()
        response = get_from_sio(sio, 'signup')
        sign_up(sio, custom = {'password':'54321aaaaaaa'})
        
        self.assertEqual(response.get(), ['password_no_match'])
        self.assertFalse(user_db.find_one({'email':'hikaridesuyoo@gmail.com'}))
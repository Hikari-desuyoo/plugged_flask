from flask_app.controllers.controller import Controller
from flask_app.models.user import User
from flask import session
from passlib.hash import pbkdf2_sha256

class UserController(Controller):
    def on_signup(self, data):
        current_user = self.get_current_user()
        if current_user: return 'already_logged'

        raw_password = data['password']
        raw_password_confirm = data['password_confirm']
        data['password'] = pbkdf2_sha256.hash(data['password'])

        user = User.new(data)
        user.validate_bad_password(raw_password)
        user.validate_password_matching(raw_password, raw_password_confirm)

        if user.save():
            user.raw_login()
            return 'success'
        else:
            return user.errors

    def on_login(self, data):
        current_user = self.get_current_user()

        if current_user: return 'failed'

        user = User.find_by(email = data.get('email'))
        if not user: return 'failed'

        return 'success' if user.login(data.get('password')) else 'failed'

    def on_logout(self):
        current_user = self.get_current_user()
        if not current_user: return 'not_logged'

        current_user.logout()
        return 'success'

    def on_disconnect(self):
        self.on_logout()

    def on_verify_email(self, data):
        current_user = self.get_current_user()
        code = data

        return 'success' if current_user.verify_email(code) else 'failed'

    def on_is_email_verified(self):
        return self.is_current_user_email_verified()

    def on_get_user_info(self):
        if not self.is_current_user_email_verified(): return
        current_user = self.get_current_user()
        
        
        return current_user.to_dict()



from flask import Flask, session
from flask_mail import Message
from passlib.hash import pbkdf2_sha256
from flask_app.models.model import Model
import uuid
import random
import pymongo
import re
import pdb

class User(Model):
  EMAIL_REGEX = '[^@]+@[^@]+\.[^@]+'
  PASSWORD_REGEX = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'

  @classmethod
  def client_input_attributes(cls):
    return ['username', 'email', 'password']

  @classmethod
  def server_input_attributes(cls):
    return {
      'online':False,
      'profile_picture': None,
      'verification_code':cls.get_random_verification_code()
    }

  @classmethod
  def get_random_verification_code(cls):
      code = ""
      for i in range(4):
        code += random.choice("0123456789")

      print( '-----------------')
      print(f'-------{code}-------')
      print( '-----------------')

      return code

  def validate(self): 
    return {
      'email_in_use' : User.find_by(email=self['email']),
      'not_email' : not re.match(self.EMAIL_REGEX, self['email']),
      'username_in_use' : User.find_by(username=self['username']),
      'blank_username' : not len(self['username']) > 0
    }

  def validate_bad_password(self, password):
    if not re.match(self.PASSWORD_REGEX, password):
      self.errors.append('bad_password')

  def validate_password_matching(self, password, password_confirm):
    if password != password_confirm:
      self.errors.append('password_no_match')

  def set_online(self):
    self['online'] = True

  def set_offline(self):
    self['online'] = False

  def send_mail_verification(self, mail):
    msg = Message('Verificação de email',
                  sender="from@example.com",
                  recipients=[self['email']])

    msg.body = f"Seu código de verificação: {self['verification_code']}"

    #mail.send(msg)
  
  def logout(self):
    self.set_offline()
    session.clear()
  
  def login(self, received_password):
    print('\n\n')
    print(self['password'])
    if pbkdf2_sha256.verify(received_password, self['password']):
        self.raw_login()
        return True
    
    return False

  def raw_login(self):
    session['current_user'] = self
    self.set_online()

  def verify_email(self, code):
    if code == self['verification_code']:
      self['verification_code'] = None
      return True
    return False

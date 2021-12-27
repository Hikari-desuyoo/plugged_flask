from flask import Flask, session
from flask_mail import Message
from flask_app.config import mongodb_settings
import uuid
import random
import pymongo
import re
import inflect
from .association_list import AssociationList

class Model:
    """
    Base class for models. Includes integration with the MongoDB database
    """
    mongodb_settings = mongodb_settings.get()
    client = pymongo.MongoClient(mongodb_settings['host'], mongodb_settings['port'])
    db = client[mongodb_settings['database']]

    p = inflect.engine()

    @classmethod
    def client_input_attributes(cls):
        """
        This method returns a list of document attributes that is allowed be modified on create by the client.
        Useful for parameter sanitization.
        """
        return []

    @classmethod
    def server_input_attributes(cls):
        """
        This method returns a dictionary of document attributes to be set
        """
        return {}

    @classmethod
    def associations(cls):
        """
        This method return a dictionary detailing associations on the model,
        being the key an attribute name, and the value a model-like class
        e.g.
        {'purchases':Purchase}
        """
        return {}

    @classmethod
    def sanitize(cls, data):
        """
        Filters client_input_attributes list's attributes from a dictionary
        """
        return {k: v for k, v in data.items() if k in cls.client_input_attributes()}

    @classmethod
    def new(cls, data={}):
        """
        Creates a new instance of the model. Won't be saved automatically.
        """
        db_document = {
        '_id': uuid.uuid4().hex
        }

        db_document.update(cls.sanitize(data))
        db_document.update(cls.server_input_attributes())

        return cls(db_document)

    @classmethod
    def get_collection_name(cls):
        """
        The collection name will always be the name of the Model class on plural form, downcased
        e.g. User -> users
        """
        return cls.p.plural(cls.__name__.lower())

    @classmethod
    def get_collection(cls):
        return cls.db[cls.get_collection_name()]

    @classmethod
    def find_by(cls, **kwargs):
        """
        Searches for a document matching the passed kwargs and returns
        a model instance if found, otherwise return None
        """
        model_object = cls.get_collection().find_one(kwargs)
        if model_object: return cls(model_object) 

    def __init__(self, db_document):
        self.errors = []
        self.db_document = db_document
        self.model_associations = self.associations()

    def to_dict(self):
        """
        Returns the document contents in dictionary form. Will omit the attribute if it's named 'password'
        """
        db_document_copy = self.db_document.copy()
        if db_document_copy.get('password'): del db_document_copy['password']
        return db_document_copy

    def __setitem__(self, key, value):
        """
        Setting a value means it will be saved to the database
        """
        self.set_document_attribute(key, value, save=True)

    def set_document_attribute(self, key, value, save=False):
        """
        Sets a value to the instance's document contents. 
        If save=True, database will be updated to the change
        """
        self.db_document[key] = value
        if not save: return
        
        self.get_collection().update_one({'_id': self.db_document['_id']},
                   {"$set": {key: value}}) 
        
    def __getitem__(self, key):
        value = self.db_document[key]
        if not key in self.model_associations.keys(): return value

        return AssociationList(key, value, self.model_associations[key], self)

    def __eq__(self, other):
        id_check = False
        class_check = False
        try:
            id_check = self['_id'] == other['_id']
            class_check = self.__class__ == other.__class__
        except:
            pass 
        return id_check and class_check

    def update(self):
        """
        Overwrites the actual document contents with the instance's document contents 
        """
        return self.get_collection().replace_one({'_id': self.db_document['_id']},
                   self.db_document) 

    def check_validation(self): 
        validations = self.validate()
        if not validations: validations = {}

        for error_name, occurred in validations.items():
            if occurred: self.errors.append(error_name)

        return not self.errors

    def validate(self): 
        """
        Model validations should be made here, by overwriting this method. 
        Additionally, it can return a dictionary, e.g. {'error_name':True, 'error_name2':False},
        where all keys with value 'True' will be added to the errors ocurred. 
        See self.check_validation() for more information.
        """
        pass

    def after_save(self): 
        """
        Runs after save method being successfully executed
        """
        pass

    def save(self):
        """
        Tries to save the model to the database for the first time. 
        It first validates the attributes, and returns wether it was saved or not.
        """
        if not self.check_validation(): return False

        insert_one = self.raw_save()
        if insert_one:
            self.after_save()
            return True

        self.errors.append('failed')
        return False

    def raw_save(self):
        """
        Saves the model to the database without any checking.
        """
        return self.get_collection().insert_one(self.db_document)


        
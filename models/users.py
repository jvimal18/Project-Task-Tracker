'''
Created on Jun 21, 2018

@author: Vimal Jay
'''
from common.database import Database
from flask import session
from builtins import staticmethod


class User(object):
    
    def __init__(self, email, password, isadmin, name, _id = None):        
        self.email = email
        self.password = password
        self.isadmin = isadmin
        self.name = name
    
    @classmethod
    def getbyname(cls, email):
        data = Database.findone(collection='users', query={"email": email })
        if data is not None:
            return cls(**data)
        else:
            print("empty")

    @classmethod
    def loginvalid(cls, email, password):
        #check user login creds are valid
        user = User.getbyname(email)
        if user is not None:
            if user.password == password: #if pass same login
                session['name'] = user.name
                session['email'] = user.email
                
                if user.isadmin == "True":
                    session['isadmin'] = "Admin"            
                else:
                    session['isadmin'] = "Normal"
                return True
        else:
            return False
            #check pass
                              
    @staticmethod
    def login(user_email):
        session['email'] = user_email
        
    @staticmethod
    def logout(user_email):
        session['email'] = None
    
    @staticmethod
    def get_alltask():
        return Database.find('Task', {})

    @staticmethod
    def gettaskbyname():
        return Database.find('Task', {'owner' : session['name']})
          
    @staticmethod
    def validatloginsession():
        if session.get('email') is not None:
            return True
        else:
            return False
        
    def create_user(self):
        Database.insert('users', self.json())
    
    @staticmethod
    def get_users(field):
        return Database.Distinct('users', field)

    def json(self):
        return {
            'email': self.email,
            'password': self.password,
            'isadmin': self.isadmin,
            'name': self.name
            }

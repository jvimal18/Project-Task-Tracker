'''
Created on Jun 21, 2018

@author: Vimal Jay
'''

import pymongo


class Database(object):
    uri = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.uri)
        Database.DATABASE = client["TaskTrack"]
    
    @staticmethod
    def insert(collection, data):
        return Database.DATABASE[collection].insert(data)

    @staticmethod
    def Distinct(collection, field):
        return Database.DATABASE[collection].distinct(field)
        
    @staticmethod
    def find(collection, query):    
        return Database.DATABASE[collection].find(query)
        
        
    @staticmethod
    def findone(collection, query):
        return Database.DATABASE[collection].find_one(query)
        
    @staticmethod
    def update(collection, query, data):
        return Database.DATABASE[collection].update_one(query, data)

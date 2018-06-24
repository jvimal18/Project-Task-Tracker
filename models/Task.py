'''
Created on Jun 21, 2018

@author: Vimal Jay
'''

from common.database import Database
from datetime import datetime


class Task(object):
    
    def __init__(self, taskname, owner, summary, managedby, percent, comments, eta, status):
        self.taskname = taskname
        self.owner = owner
        self.summary = summary
        self.managedby = managedby
        self.percent = percent
        self.comments = comments
        self.eta = eta
        self.status = status
        self.date= datetime.now().strftime("%Y-%m-%d")
        
    def save_to_db(self):
        query = self.json()
        query.update({'createddate': self.date})
        Database.insert('Task', query)
        print("database")

    @staticmethod
    def update_dbdoc(taskname, query):
        return Database.update(collection='Task', query={'taskname': taskname}, data={"$set": query})

    def json(self):
        return {
            'taskname': self.taskname,
            'owner': self.owner,
            'summary': self.summary,
            'managedby': self.managedby,
            'percent': self.percent,
            'comments': self.comments,
            'eta': self.eta,
            'status': self.status,
            }

    @staticmethod
    def get_from_mongo_bytaskname(taskname):
        return Database.find(collection='Task', query={'taskname': taskname})

    @staticmethod
    def remove_empty_from_dict(dic):
        if type(dic) is dict:
            return dict((k, Task.remove_empty_from_dict(v)) for k, v in dic.items() if v and Task.remove_empty_from_dict(v))
        elif type(dic) is list:
            return [Task.remove_empty_from_dict(v) for v in dic if v and Task.remove_empty_from_dict(v)]
        else:
            return dic


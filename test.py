import pymongo
from common.database import Database
from models.users import User


d = {'taskname': 'this is test', 'owner': 'abc', 'summary': '', 'b_edit_Task': '', 'percent': '0', 'ETA': '',
     'Manageby': '', 'comment': ''}



def remove_empty_from_dict(d):
    if type(d) is dict:
        return dict((k, remove_empty_from_dict(v)) for k, v in d.items() if v and remove_empty_from_dict(v))
    elif type(d) is list:
        return [remove_empty_from_dict(v) for v in d if v and remove_empty_from_dict(v)]
    else:
        return d

print(remove_empty_from_dict(d))
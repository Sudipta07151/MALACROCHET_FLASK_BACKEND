# from flask_pymongo import PyMongo
# import os

# class MongoConnect:
#     def __init__(self,app):
#         self.mongo = PyMongo(app,uri=os.getenv('MONGO_URI'))


from flask_pymongo import PyMongo
import os

class MongoConnect:
    __db_instance=None
    def __init__(self,app):
        try:
            if MongoConnect.__db_instance!=None:
                raise Exception("Database instance already present and cant be instantiated again!")
            self.db= PyMongo(app,uri=os.getenv('MONGO_URI')).db
            MongoConnect.__db_instance=self
            print('CONNECTION SUCCESSFUL')
        except:
            print('CONNECTION FAILED!')
    @staticmethod
    def getDatabaseInstance():
        if MongoConnect.__db_instance==None:
            raise Exception("No Database Instance Present! Try Creating one")
        return MongoConnect.__db_instance

    
from flask_restful import Resource,request
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
import sys
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from bson.json_util import dumps
from bson.objectid import ObjectId




from models.uploaditem import UploadItem
sys.path.append('../database')

from . import data_service_api
from database.mongoConnect import MongoConnect


class GetAllData(Resource): 
    def __init__(self,**kwargs):
        self.db=kwargs['db']           
    def get(self):
        cursor=self.db.items.find()
        json_data=dumps(list(cursor))
        return json_data


class GetSingleImage(Resource): 
    def __init__(self,**kwargs):
        self.db=kwargs['db']           
    def get(self,oid):
        print(ObjectId(oid))
        cursor=self.db.items.find_one({"_id": ObjectId(oid)})
        print(cursor)
        json_data=dumps(list(cursor))
        print(json_data)
        return dumps(cursor)


db_instance=MongoConnect.getDatabaseInstance()


data_service_api.add_resource(GetAllData, '/',resource_class_kwargs={'db': db_instance.db})
data_service_api.add_resource(GetSingleImage, '/singlefile/<string:oid>',resource_class_kwargs={'db': db_instance.db})



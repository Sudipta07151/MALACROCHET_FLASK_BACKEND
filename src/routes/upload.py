from email import message
import json
from flask_restful import Resource,request
import cloudinary
import cloudinary.uploader
from cloudinary.uploader import upload
import cloudinary.api
from cloudinary.utils import cloudinary_url
import os
from bson.json_util import dumps
from bson.objectid import ObjectId

class Upload(Resource):
    def __init__(self,**kwargs):
        self.db=kwargs['db']
    def post(self):
        cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
        file_to_upload = request.files['file']
        #name_of_file=request.form['name']
        tag_of_file=request.form['tag']
        #print(file_to_upload)

        if file_to_upload:
            upload_result = cloudinary.uploader.upload(file_to_upload)
            #print(upload_result)
            #self.db.items.insert_one({'name':name_of_file,'tag':tag_of_file,'image_url':upload_result['url']})
            self.db.items.insert_one({'tag':tag_of_file,'image_url':upload_result['url']})
            return {'message': 'success','data':upload_result['url']},200
        return {'message':'fail'}, 400

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


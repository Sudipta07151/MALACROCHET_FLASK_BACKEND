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

from . import upload_service_api
from database.mongoConnect import MongoConnect

from bson.json_util import dumps

class UploadAngular(Resource):
    def __init__(self,**kwargs):
        self.db=kwargs['db']
        print(self.db)
    def post(self):
        cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
        try:
            file_to_upload = request.files['file']
            tag_of_file=request.form['category']
            name_of_file=request.form['name']
            price=request.form['price']
            #return {'message':'SUCCESS'},200

            if file_to_upload:
                upload_result = cloudinary.uploader.upload(file_to_upload)
                upload_item=UploadItem(picture=upload_result['url'],category=tag_of_file,name=name_of_file,price=price)
                upload_obj=upload_item.getUploadItem()
                #print(upload_result)
                # self.db.items.insert_one({'name':name_of_file,'tag':tag_of_file,'price':price,'image_url':upload_result['url']})
                print(upload_obj)
                self.db.items.insert_one(upload_obj)
                return {'message': 'success','data':upload_result['url']},200
        except:
            return {'message':'fail'}, 400

class Upload(Resource):
    def __init__(self,**kwargs):
        self.db=kwargs['db']
    @jwt_required()
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

db_instance=MongoConnect.getDatabaseInstance()


upload_service_api.add_resource(Upload, '/upload',resource_class_kwargs={'db': db_instance.db})
upload_service_api.add_resource(UploadAngular, '/uploadfile',resource_class_kwargs={'db': db_instance.db})

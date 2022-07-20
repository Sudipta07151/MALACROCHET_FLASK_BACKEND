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
import base64 
from Cryptodome.Cipher import AES 
from Cryptodome.Util.Padding import pad,unpad
import json


from models.uploaditem import UploadItem
sys.path.append('../database')
sys.path.append('../../otpservice')
from otpservice.otp import Otp
sys.path.append('../../sendinblueservice')
from sendinblueservice.sendinblue import sendinblue

from . import utility_service_api
from database.mongoConnect import MongoConnect

from bson.json_util import dumps

class OtpVerification(Resource):
    def __init__(self,**kwargs):
        self.db=kwargs['db']
    def post(self):
        try:
            email=request.json['email']
            otp_obj=Otp()
            otp_number=otp_obj.generateOTP()
            sendinblue_obj=sendinblue()
            send_data=f"OTP VERIFY NUMBER: {otp_number}"
            sendinblue_obj.run_service(email,send_data)
            print(otp_number)
            return {'Otp': True,"message_data":"Otp Generated","orders":dumps(otp_number)}
        except:
            return {'Otp': False,"message_data":"Otp Generation Failed"}

class EnterComment(Resource): 
    def __init__(self,**kwargs):
        self.db=kwargs['db']           
    def post(self,oid):
        print(ObjectId(oid))
        comment=request.form['comment']
        userID=request.form['userID']
        commentId=self.db.comments.insert_one({'comment':comment,'user':userID})
        cursor=self.db.items.find_one_and_update({"_id": ObjectId(oid)},{'$push':{'comments':dumps(commentId.inserted_id)}},return_document=ReturnDocument.AFTER)
        print(cursor)
        json_data=dumps(list(cursor))
        print(json_data)
        return dumps(cursor)
    
    def get(self,oid):
        print(ObjectId(oid))
        try:
            cursor=self.db.items.find({"_id": ObjectId(oid)},{"comments":1,"_id":0})
            json_data=dumps(list(cursor))
            comment_list=[]
            print('data got:',json.loads(json_data)[0]['comments'])
            for comment in json.loads(json_data)[0]['comments']:
                print('comment id',json.loads(comment)['$oid'])
                comment_data=self.db.comments.find({"_id": ObjectId(json.loads(comment)['$oid'])})
                print('got comment data:',comment_data)
                comment_list.append(dumps(comment_data))
            return {"message":"success getting comments","comments":dumps(comment_list)}
        except:
            return {"message":'couldnt fetch comments',"comments":dumps([])}

class EncryptPassword(Resource): 
    def __init__(self,**kwargs):
        self.db=kwargs['db']           
    def post(self):
        try:
            password=request.json['password']
            print(password)
            key = 'AAAAAAAAAAAAAAAA'
            iv =  'BBBBBBBBBBBBBBBB'.encode('utf-8')
            data= pad(password.encode(),16)
            cipher = AES.new(key.encode('utf-8'),AES.MODE_CBC,iv)
            encrypted=base64.b64encode(cipher.encrypt(data))
            print(str(encrypted))
            return {"message":'encytion successful',"encrytion":"true","password_enc":dumps(str(encrypted))}
        except:
            return {"message":'couldnt encrypt',"encrytion":'false'}



db_instance=MongoConnect.getDatabaseInstance()

utility_service_api.add_resource(OtpVerification, '/otpverify',resource_class_kwargs={'db': db_instance.db})
utility_service_api.add_resource(EnterComment, '/comment/<string:oid>',resource_class_kwargs={'db': db_instance.db})
utility_service_api.add_resource(EncryptPassword, '/encryptpassword',resource_class_kwargs={'db': db_instance.db})


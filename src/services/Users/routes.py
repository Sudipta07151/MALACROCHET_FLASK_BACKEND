from flask_restful import Resource,request
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
import sys
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import base64 
from Cryptodome.Cipher import AES 
from Cryptodome.Util.Padding import pad,unpad
from pymongo import ReturnDocument
from bson.json_util import dumps
from bson.objectid import ObjectId


from models.user import User
sys.path.append('../database')

from . import user_service_api
from database.mongoConnect import MongoConnect


class SignUpUser(Resource):
    def __init__(self,**kwargs):
        self.db=kwargs['db']
    def post(self):
        email=request.form['email']
        name=request.form['name']
        password=request.form['password']
        isAdmin=request.form['isAdmin']
        user=User(email=email,name=name,password=password,isAdmin=isAdmin)
        user_obj=user.getUser()
        if password=='' or name=='' or email=='':
            return {'upload': False,"message_data":"some fields are empty"}
        try:
            document=self.db.users.find_one({"email":email})
            print(document)
            if document==None:
                self.db.users.insert_one(user_obj)
                return {'upload':True,"message_data":"successfully registered"}
            else:
                return {'upload': False, "message_data":"email already present"}    
        except:
            return {'upload': False,"message_data":"could not upload"}


class LoginUser(Resource):
    def __init__(self,**kwargs):
        self.db=kwargs['db']
    def post(self):
        email=request.form['email']
        password=request.form['password']
        if password=='' or email=='':
            return {'login': False,"message_data":"some fields are empty"}
        try:
            document=self.db.users.find_one({"email":email})
            #print('document found',document)

            if document!=None:
                #password decrypt
                iv='BBBBBBBBBBBBBBBB'.encode('utf-8')
                enc=base64.b64decode(document['password'])
                cipher=AES.new('AAAAAAAAAAAAAAAA'.encode('utf-8'), AES.MODE_CBC, iv)
                password_decrypted=unpad(cipher.decrypt(enc),16).decode("utf-8")
                # print(document)
                #print(password_decrypted.decode("utf-8"))

                if password_decrypted==password:
                    return {'login':True,"message_data":"successfully logged in","login_data":dumps({"id":document['_id'],"name":document["name"],"email":document["email"]})}
                return {'login': False, "message_data":"invalid credentials"}
            else:
                return {'login': False, "message_data":"invalid credentials"}    
        except:
            return {'login': False,"message_data":"could not login"}

class SignUpAdmin(Resource):
    def __init__(self,**kwargs):
        self.db=kwargs['db']
    def post(self):
        email=request.form['email']
        password=request.form['password']
        adminKey=request.form['adminKey']
        user=User(email=email,name="Admin User",password=password,isAdmin=True)
        user_obj=user.getUser()
        print('SignUpAdmin HIT',password,email,adminKey)
        if email=='' or password=='' or adminKey=='':
            return {'signup': False,"message_data":"some fields are empty"}
        if adminKey!=os.getenv("ADMIN_KEY"):
            return {'signup':False,"message_data":"could not sign up, invalid key"}
        try:
            document=self.db.users.find_one({"email":email})
            print(document)
            if document==None:
                self.db.users.insert_one(user_obj)
                access_token = create_access_token(identity={"email":email})
                return {'signup':True,"message_data":"successfully registered admin user","access_token":access_token}
            else:
                return {'signup': False, "message_data":"email already present"}    
        except:
            return {'upload': False,"message_data":"could not upload"}

class SignUpAdminAngular(Resource):
    def __init__(self,**kwargs):
        self.db=kwargs['db']
    def post(self):
        email=request.json['email']
        password=request.json['password']
        adminKey=request.json['adminKey']
        user=User(email=email,name="Admin User",password=password,isAdmin=True)
        user_obj=user.getUser()
        print('SignUpAdmin HIT',password,email,adminKey)
        if email=='' or password=='' or adminKey=='':
            return {'signup': False,"message_data":"some fields are empty"}
        if adminKey!=os.getenv("ADMIN_KEY"):
            return {'signup':False,"message_data":"could not sign up, invalid key"}
        try:
            document=self.db.users.find_one({"email":email})
            print(document)
            if document==None:
                self.db.users.insert_one(user_obj)
                access_token = create_access_token(identity={"email":email})
                return {'signup':True,"message_data":"successfully registered admin user","access_token":access_token}
            else:
                return {'signup': False, "message_data":"email already present"}    
        except:
            return {'upload': False,"message_data":"could not upload"}

class LoginAdminUser(Resource):
    def __init__(self,**kwargs):
        self.db=kwargs['db']
    def post(self):
        email=request.form['email']
        password=request.form['password']
        adminKey=request.form['adminKey']
        if password=='' or email=='':
            return {'login': False,"message_data":"some fields are empty"}
        if adminKey!=os.getenv("ADMIN_KEY"):
            return {'login': False,"message_data":"invalid admin key"}
        try:
            document=self.db.users.find_one({"email":email,"isAdmin":True})
            #print('document found',document)

            if document!=None:
                #password decrypt
                iv='BBBBBBBBBBBBBBBB'.encode('utf-8')
                enc=base64.b64decode(document['password'])
                cipher=AES.new('AAAAAAAAAAAAAAAA'.encode('utf-8'), AES.MODE_CBC, iv)
                password_decrypted=unpad(cipher.decrypt(enc),16).decode("utf-8")
                # print(document)
                #print(password_decrypted.decode("utf-8"))

                if password_decrypted==password:
                    access_token = create_access_token(identity={"email":email})
                    return {'login':True,"access_token":access_token,"message_data":"successfully logged in","login_data":dumps({"id":document['_id'],"name":document["name"]})}

                return {'login': False, "message_data":"invalid credentials"}
            else:
                return {'login': False, "message_data":"invalid credentials"}    
        except:
            return {'login': False,"message_data":"could not login"}

class LoginAdminUserAngular(Resource):
    def __init__(self,**kwargs):
        self.db=kwargs['db']
    def post(self):
        email=request.json['email']
        password=request.json['password']
        adminKey=request.json['adminKey']
        if password=='' or email=='':
            return {'login': False,"message_data":"some fields are empty"},401
        if adminKey!=os.getenv("ADMIN_KEY"):
            return {'login': False,"message_data":"invalid admin key"},401
        try:
            document=self.db.users.find_one({"email":email,"isAdmin":True})
            print('document found',document)

            if document!=None:
                #password decrypt
                iv='BBBBBBBBBBBBBBBB'.encode('utf-8')
                enc=base64.b64decode(document['password'])
                cipher=AES.new('AAAAAAAAAAAAAAAA'.encode('utf-8'), AES.MODE_CBC, iv)
                password_decrypted=unpad(cipher.decrypt(enc),16).decode("utf-8")
                # print(document)
                #print(password_decrypted.decode("utf-8"))

                if password_decrypted==password:
                    access_token = create_access_token(identity={"email":email})
                    return {'login':True,"access_token":access_token,"message_data":"successfully logged in","login_data":dumps({"id":document['_id'],"name":document["name"]})},200

                return {'login': False, "message_data":"invalid credentials"},401
            else:
                return {'login': False, "message_data":"invalid credentials"},401    
        except:
            return {'login': False,"message_data":"could not login"},401


db_instance=MongoConnect.getDatabaseInstance()


user_service_api.add_resource(SignUpUser, '/signup',resource_class_kwargs={'db': db_instance.db})
user_service_api.add_resource(LoginUser, '/login',resource_class_kwargs={'db': db_instance.db})
user_service_api.add_resource(SignUpAdmin, '/signupadmin',resource_class_kwargs={'db': db_instance.db})
user_service_api.add_resource(SignUpAdminAngular, '/signupadminangular',resource_class_kwargs={'db': db_instance.db})
user_service_api.add_resource(LoginAdminUser, '/loginadmin',resource_class_kwargs={'db': db_instance.db})
user_service_api.add_resource(LoginAdminUserAngular, '/loginadminangular',resource_class_kwargs={'db': db_instance.db})


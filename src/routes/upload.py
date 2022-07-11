from audioop import add
from cmath import pi
import json
from pydoc import doc
import string
from urllib import response

from flask_restful import Resource,request
import cloudinary
import cloudinary.uploader
from cloudinary.uploader import upload
import cloudinary.api
from cloudinary.utils import cloudinary_url
import os
from bson.json_util import dumps
from bson.objectid import ObjectId
from models.user import User
from models.product import Product
from models.uploaditem import UploadItem



import sys
sys.path.append('../../twilioservice')
from twilioservice.TwilioMsgService import send_sms
sys.path.append('../../sendinblueservice')
from sendinblueservice.sendinblue import sendinblue
sys.path.append('../../otpservice')
from otpservice.otp import Otp

import base64 
from Cryptodome.Cipher import AES 
from Cryptodome.Util.Padding import pad,unpad
from pymongo import ReturnDocument

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required




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

class UploadAngular(Resource):
    def __init__(self,**kwargs):
        self.db=kwargs['db']
   
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


class PlaceOrder(Resource):
    def __init__(self,**kwargs):
        self.db=kwargs['db']
    def post(self):
        fname=request.form['fname']
        lname=request.form['lname']
        address=request.form['address']
        city=request.form['city']
        landmark=request.form['landmark']
        state=request.form['state']
        pin=request.form['pin']
        phone=request.form['phone']
        products=request.form['products']
        userId=request.form["userid"]
        #print('userid:',ObjectId(userId))
        try:
            document=self.db.users.find_one_and_update({"_id":ObjectId(userId)},{'$push':{'orders':dumps(products)}},return_document=ReturnDocument.AFTER)
            print('user doc',document)
            if fname=='' or lname=='' or address=='' or city=='' or landmark=='' or state=='' or pin=='' or phone=='' or products=='':
                return {'upload': False,"message_data":"some fields are empty"}
            try:
                product=Product(fname=fname,lname=lname,address=address,pin=pin,products=products,phone=phone,landmark=landmark,state=state,city=city,userId=userId)
                product_obj=product.getProduct()
                placed_order=self.db.products.insert_one(product_obj)
                print('placed_order:',placed_order.inserted_id)
                self.db.users.find_one_and_update({"_id":ObjectId(userId)},{'$push':{'orderslist':placed_order.inserted_id}},return_document=ReturnDocument.AFTER)
                send_sms(body=f"AN ORDER HAS BEEN PLACED BY {fname+lname} PHONE: {phone} ADDRESS: {address} PIN: {pin} ORDERID: {placed_order.inserted_id}")
                sendinblue_obj=sendinblue()
                send_data=f"ORDER PLACED SUCCESSFULLY , WE WILL DISPATCH ORDER SOON . ORDER ID {placed_order.inserted_id}"
                sendinblue_obj.run_service(document['email'],send_data)
                sendinblue_obj.create_contact()
                return {'upload':True,"message_data":"successfully ordered","orderid":dumps(placed_order.inserted_id)}
            except:
                return {'upload': False,"message_data":"could not place order"}
        except:
            return {'upload': False,"message_data":"must be logged in to place order"}

class YourOrders(Resource):
    def __init__(self,**kwargs):
        self.db=kwargs['db']
    def post(self):
        try:
            id=request.json['userID']
            print(id)
            document=self.db.users.find_one({"_id":ObjectId(id)},{"orders":1})
            print(document)
            return {'found': False,"message_data":"orders found","orders":dumps(document)}
        except:
            return {'upload': False,"message_data":"must be logged in to place order"}

class AllOrders(Resource):
    def __init__(self,**kwargs):
        self.db=kwargs['db']
    def post(self):
        try:
            startPage=request.json['startPage']
            endPage=request.json['endPage']
            pageLimit=request.json['pageLimit']
            print(startPage,endPage,pageLimit)
            print(type(startPage))
            cursor=self.db.products.find({"$or":[{ "approved" : False },{ "approved" : {'$exists':False}}]}).skip(startPage).limit(pageLimit)
            ttlcnt=self.db.products.count_documents({"$or":[{ "approved" : False },{ "approved" : {'$exists':False}}]})
            # print('ttllcnt',ttlcnt)
            allorders=list(cursor)
            allOrdersData={}
            for order in allorders:
                orders=order['order']
                # print(str(order['_id']))
                items=json.loads(json.loads(orders['products']))
                details=order['details']
                productsOrdered=[]
                for item in items:
                    if item['_id']:
                        # print(item['_id']['$oid'])
                        # productsOrdered.append(item['_id']['$oid'])
                        productsOrdered.append(item)
                        #print(productsOrdered,details)
                allOrdersData[str(order['_id'])]={'oid':str(order['_id']),'details':details,'products':productsOrdered}
            #print(allOrdersData)
            #print(type(allOrdersData))
            return {'found': True,"message_data":"orders found","orders":dumps(allOrdersData),"ttlcnt":ttlcnt}
        except:
            return {'found': False,"message_data":"must be logged in to find all order"}

class ApproveOrder(Resource):
    def __init__(self,**kwargs):
        self.db=kwargs['db']
    def put(self):
        try:
            oid=request.json['oid']
            self.db.products.find_one_and_update({"_id": ObjectId(oid)},{ '$set': { "approved" : True} })
            return {'message':'Status approved sucessfully'},200 
        except:
            {'message':'Fail to approve status'},500

class DispatchedOrders(Resource):
    def __init__(self,**kwargs):
        self.db=kwargs['db']
    def get(self):
        try:
            cursor=self.db.products.find({ "approved" : True})
            allorders=list(cursor)
            allOrdersData={}
            for order in allorders:
                orders=order['order']
                # print(str(order['_id']))
                items=json.loads(json.loads(orders['products']))
                details=order['details']
                productsOrdered=[]
                for item in items:
                    if item['_id']:
                        # print(item['_id']['$oid'])
                        # productsOrdered.append(item['_id']['$oid'])
                        productsOrdered.append(item)
                        #print(productsOrdered,details)
                allOrdersData[str(order['_id'])]={'oid':str(order['_id']),'details':details,'products':productsOrdered}
            return {'found': True,"message_data":"orders found","orders":dumps(allOrdersData)},200
        except:
            {'message':'Fail to get data'},500

class GetOrdersCount(Resource):
    def __init__(self,**kwargs):
        self.db=kwargs['db']
    def get(self):
        try:
            ttlcntNotApproved=self.db.products.count_documents({"$or":[{ "approved" : False },{ "approved" : {'$exists':False}}]})
            ttlcntApproved=self.db.products.count_documents({ "approved" : True })
            ttlcntAll=self.db.products.count_documents({})
            print(ttlcntNotApproved,ttlcntAll)
            return {'found': True,"message_data":"found","ttlcntNotApproved":dumps(ttlcntNotApproved),"ttlcntAll":dumps(ttlcntAll),"ttlcntApproved":dumps(ttlcntApproved)},200
        except:
            {'message':'Fail to get data'},500



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


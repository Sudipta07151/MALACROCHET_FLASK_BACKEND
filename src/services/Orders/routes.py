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
from pymongo import ReturnDocument
import json




from models.uploaditem import UploadItem
sys.path.append('../database')
sys.path.append('../../twilioservice')
from twilioservice.TwilioMsgService import send_sms
sys.path.append('../../sendinblueservice')
from sendinblueservice.sendinblue import sendinblue

from models.product import Product


from . import order_service_api
from database.mongoConnect import MongoConnect


from bson.json_util import dumps

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


db_instance=MongoConnect.getDatabaseInstance()

order_service_api.add_resource(PlaceOrder, '/placeorder',resource_class_kwargs={'db': db_instance.db})
order_service_api.add_resource(YourOrders, '/yourorder',resource_class_kwargs={'db': db_instance.db})
order_service_api.add_resource(AllOrders, '/allorders',resource_class_kwargs={'db': db_instance.db})
order_service_api.add_resource(ApproveOrder, '/approveorderstatus',resource_class_kwargs={'db': db_instance.db})
order_service_api.add_resource(DispatchedOrders, '/dispatchedorders',resource_class_kwargs={'db': db_instance.db})
order_service_api.add_resource(GetOrdersCount, '/getorderscount',resource_class_kwargs={'db': db_instance.db})

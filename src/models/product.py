from audioop import add
from bson.json_util import dumps
import json

class Product:
    def __init__(self,lname='',fname='',address='',state='',city='',products=[],phone='',pin='',landmark='',userId='',approved=False):
        self.fname=fname
        self.lname=lname
        self.address=address
        self.phone=phone
        self.produts=products
        self.pin=pin
        self.city=city,
        self.state=state
        self.landmark=landmark
        self.userId=userId
        self.approved=approved
        print('Product',json.loads(products))
    def getProduct(self):
        product_obj = {"details":{"fname":self.fname,"lname":self.lname,"address":self.address,"pin":self.pin,"landmark":self.landmark,"state":self.state,"phone":self.phone,"city":self.city,"approved":self.approved},"order":{"products":dumps(self.produts)},"userid":self.userId}
        return product_obj
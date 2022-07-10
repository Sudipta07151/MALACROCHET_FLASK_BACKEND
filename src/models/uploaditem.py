import json

class UploadItem:
    def __init__(self,price='',category='',name='',picture=None):
        self.price=price
        self.category=category
        self.picture=picture
        self.name=name
    def getUploadItem(self):
        item_obj = {"name":self.name,"tag":self.category,'image_url': self.picture,"price":self.price}
        return item_obj
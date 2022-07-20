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






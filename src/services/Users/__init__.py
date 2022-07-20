from flask import Blueprint
from flask_restful import Api

user_service=Blueprint('user_service',__name__)
user_service_api=Api(user_service)

from . import routes


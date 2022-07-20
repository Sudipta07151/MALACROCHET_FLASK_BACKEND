from flask import Blueprint
from flask_restful import Api

data_service=Blueprint('data_service',__name__)
data_service_api=Api(data_service)

from . import routes


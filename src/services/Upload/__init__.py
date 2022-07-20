from flask import Blueprint
from flask_restful import Api

upload_service=Blueprint('upload_service',__name__)
upload_service_api=Api(upload_service)

from . import routes


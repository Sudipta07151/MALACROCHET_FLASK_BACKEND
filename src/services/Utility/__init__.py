from flask import Blueprint
from flask_restful import Api

utility_service=Blueprint('utility_service',__name__)
utility_service_api=Api(utility_service)

from . import routes


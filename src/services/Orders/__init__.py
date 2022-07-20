from flask import Blueprint
from flask_restful import Api

order_service=Blueprint('order_service',__name__)
order_service_api=Api(order_service)

from . import routes


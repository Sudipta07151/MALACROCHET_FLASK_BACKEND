from .Upload import upload_service
from .Users import user_service
from .Data import data_service
from .Orders import order_service
from .Utility import utility_service

class Services:
    def __init__(self,app) -> None:
        app.register_blueprint(upload_service)
        app.register_blueprint(user_service)
        app.register_blueprint(data_service)
        app.register_blueprint(order_service)
        app.register_blueprint(utility_service)
        


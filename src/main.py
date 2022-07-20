from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from dotenv import load_dotenv,dotenv_values
import sys
import os

from flask_jwt_extended import JWTManager

#importing routes file
sys.path.append('./routes')
sys.path.append('./database')


env=load_dotenv()
app = Flask(__name__)
# api = Api(app)
CORS(app)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

from database.mongoConnect import MongoConnect

try:
    db=MongoConnect(app=app)
except Exception:
    print(Exception)


config = dotenv_values(".env") 
#print(config)

from services import Services
Services(app=app)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from dotenv import load_dotenv,dotenv_values
import sys



#importing routes file
sys.path.append('./routes')
sys.path.append('./database')

from routes.upload import Upload,GetAllData
from database.mongoConnect import MongoConnect


env=load_dotenv()
app = Flask(__name__)
api = Api(app)
CORS(app)


try:
    mongo=MongoConnect(app=app).mongo
    db=mongo.db
    print('CONNECTION SUCCESSFUL')
except:
    print('CONNECTION FAILED!')

config = dotenv_values(".env") 
#print(config)

api.add_resource(Upload, '/upload',resource_class_kwargs={'db': db})
api.add_resource(GetAllData, '/',resource_class_kwargs={'db': db})

if __name__ == '__main__':
    app.run(debug=True)

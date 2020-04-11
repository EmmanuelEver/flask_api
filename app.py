from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT
from resources.user import Register
from security import authenticate, identity
from resources.item import Item, ItemList
from datetime import timedelta
from resources.store import Store, StoreList

app  			 = Flask(__name__)
app.secret_key	 = "dalbong"
api 		     = Api(app)
jwt 		     = JWT(app, authenticate, identity)
app.config['SQLALCHEMY_DATABASE_URI'] 			= 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']    = False
app.config['JWT_EXPIRATION_DELTA'] 				= timedelta(seconds =1800)



api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/itemlist')
api.add_resource(Register, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/storelist')

if '__main__' == __name__:
	from db import db
	db.init_app(app)
	app.run()
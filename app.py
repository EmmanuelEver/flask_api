import os
from flask import Flask, request
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import Register, User, UserLogin, UserLogout, TokenRefresh, UserList
from resources.item import Item, ItemList
from datetime import timedelta
from resources.store import Store, StoreList
from blacklist import BLACKLIST
from flask_cors import CORS, cross_origin

app  			 = Flask(__name__)
app.secret_key	 = "dalbong"
api 		     = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] 			= os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']    = False
app.config['JWT_EXPIRATION_DELTA'] 				= timedelta(seconds =100)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt 		     = JWTManager(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})


@jwt.user_claims_loader
def add_jwt_claims(identity):
	if identity == 1:
		return {"isAdmin" : True}
	return {"isAdmin" : False}

@jwt.token_in_blacklist_loader
def blacklist_token(decryted_key):
	jti = decryted_key['jti']
	return jti in BLACKLIST

@jwt.expired_token_loader
def expired_token():
	return jsonify({
		"description" : f"The {expired_token} is expired, Please Login again",
		"error"   : "expired token"
	})

@jwt.revoked_token_loader
def revoke_token():
	return jsonify({
			"description" : "Sorry, Your token has been revoked",
			"error"   : "Revoked Token"
		})

@jwt.unauthorized_loader
def unauthorized_loader():
	return jsonify({
			"description" : "Login first to be able to access this page",
			"error"	  : "unauthorized access"
		}), 401

@jwt.needs_fresh_token_loader
def need_fresh_token():
	return jsonify({
			"description" : "For Security Purposes, We need you to enter your password",
			"error" 	: "Fresh_Token_required"
		})



api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/itemlist')
api.add_resource(Register, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/storelist')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/Login')
api.add_resource(UserLogout, '/Logout')
api.add_resource(TokenRefresh, '/Refresh')
api.add_resource(UserList, '/Userlist')

if '__main__' == __name__:
	from db import db
	db.init_app(app)
	app.run()
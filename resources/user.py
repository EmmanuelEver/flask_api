from flask_restful import Resource,request,reqparse
from models.user   import UserModel
from flask_jwt_extended import (
			create_access_token,
			create_refresh_token,
		    jwt_refresh_token_required,
	   	    get_jwt_identity,
	   	    jwt_required,
	   	    get_raw_jwt
   		)
from werkzeug.security import safe_str_cmp
from blacklist 		import BLACKLIST



_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
			"username",
		 	type = str,
	     	required = True,
		    help="field cannot be empty"
		    )
_user_parser.add_argument(
			"password",
			 type = str,
		  	 required = True,
		     help = "Field cannot be empty"
		     )


class Register(Resource):	


	def post(self):
		data 		= _user_parser.parse_args()
		if UserModel.check_username(data['username']):
			return {"message" : "username already exist, try another one"}, 404
		user = UserModel(**data)
		user.save_to_db()
		return {'user' : data, 'message': "succesfully added new user"}, 201



class User(Resource):

	@classmethod
	def get(cls, user_id):
		user = UserModel.check_id(user_id)
		if user:
			return user.json()
		return {"message" : "Sorry, User not found"}


	@classmethod
	def delete(cls, user_id):
		user = UserModel.check_id(user_id)
		if user:
			user.delete_from_db()
			return {"message" : "user deleted"}
		return {"message" : "User doesn't exist"}

class UserLogin(Resource):

		def post(self):
			data = _user_parser.parse_args()
			user = UserModel.check_username(data['username'])
			if safe_str_cmp(user.password, data['password']):
				access_token = create_access_token(identity=user.id, fresh = True)
				refresh_token = create_refresh_token(user.id)
				return {
						"access_token" : access_token,
						"refresh_token" : refresh_token,
						"user_id"		:user.id
					}, 201

			return {"message":"Invalid Crederntials"}, 401


class UserLogout(Resource):
	@jwt_required
	def post(self):
		jti = get_raw_jwt()['jti']
		BLACKLIST.add(jti)
		print(BLACKLIST)
		return {
			"message" : "User succesfully logged out"
		}, 201

class TokenRefresh(Resource):
	@jwt_refresh_token_required
	def post(self):
		current_user = get_jwt_identity()
		new_token  = create_access_token(identity=current_user, fresh = False)
		return {
			"access_token" : new_token
		}, 200

class UserList(Resource):
	@jwt_required
	def get(self):
		user = get_jwt_identity()
		if user:
			users = [user.json() for user in UserModel.query.all()]
			return {"users", users},200
		return {"message" : "Please login to see details"}
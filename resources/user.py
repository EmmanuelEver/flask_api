from flask_restful import Resource,request,reqparse
from models.user   import UserModel


class Register(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument("username", type = str, required = True, help="field cannot be empty")
	parser.add_argument("password", type = str, required = True , help = "Field cannot be empty")


	def post(self):
		data 		= Register.parser.parse_args()
		if UserModel.check_username(data['username']):
			return {"message" : "username already exist, try another one"}, 404
		user = UserModel(**data)
		user.save_to_db()
		return {'user' : data, 'message': "succesfully added new user"}, 201
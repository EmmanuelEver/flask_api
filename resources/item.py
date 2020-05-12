from flask_restful import Resource,reqparse
from flask_jwt_extended import (
			jwt_required,
			get_jwt_claims,
			get_jwt_identity,
	   		jwt_optional,
		    fresh_jwt_required
	    )
from models.item import ItemModel
from models.user import UserModel



class Item(Resource):
	parser = reqparse.RequestParser()

	parser.add_argument(
			"price", 
			type = float, 
			required = True, 
			help = "This field is required"
			)
	parser.add_argument(
			"name",
			type = str,
			required = True,
			help = "This field is required"
		)
	parser.add_argument(
			"store_id",
			type = int,
			required = True,
			help = "item needs to have a store_id"
		)



	@jwt_optional
	def get(self, name):
		user = get_jwt_identity()
		item = ItemModel.find_name(name)
		if user:
			print(user)
			if item:
				return item.json(), 200
			return {"message" : "item not found"}, 402
		return {"item" : item.name}

	@fresh_jwt_required
	def post(self,name):
		item = ItemModel.find_name(name)
		if item:
			return {f"message" :"Sorry the item {name} already existed" }, 400
		data = Item.parser.parse_args()
		item = ItemModel(**data)
		try:		
			item.save_to_db()
		except:
			return {'message' : 'Sorry, and error appeared on our part'}, 500
		return item.json(), 201
		
	@fresh_jwt_required
	def delete(self, name):
		item = ItemModel.find_name(name)
		if item:
			item.delete_from_db()
			return{"message" : "Item succesfully deleted"}
		return {f'message': 'No such {name} item in the database'}

	@fresh_jwt_required
	def put(self, name):
		data = Item.parser.parse_args()
		item = ItemModel.find_name(name)
		if item:
			try:
				item = ItemModel(**data)
				item.save_to_db()
				return item.json(), 200
			except:
				return {'message' : "Sorry an error occured"}, 505
		else:
			try:	
				item = ItemModel(**data)
				item.save_to_db()
				return {'message' : 'item succesfully added'}, 201
			except:
				return {'message' : 'Sorry, and error appeared on our part'}, 500

class ItemList(Resource):

	@jwt_optional
	def get(self):
		user = get_jwt_identity()
		items = [item.json() for item in ItemModel.query.all()]
		if user:
			return {"items" : items}, 200
		return {"items" :[item["name"] for item in items], "message" : "Log in to see more details"}
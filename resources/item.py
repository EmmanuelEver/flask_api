from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel



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



	@jwt_required()
	def get(self, name):
		item = ItemModel.find_name(name)
		if item:
			return item.json(), 200
		return {"message" : "item not found"}, 402

	@jwt_required()
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

	def delete(self, name):
		item = ItemModel.find_name(name)
		if item:
			item.delete_from_db()
		return {f'message': 'No such {name} item in the database'}

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
	@jwt_required()
	def get(self):
		return {"items" :[x.json() for x in ItemModel.query.all()]}
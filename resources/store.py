from flask_restful import Resource
from models.store import StoreModel
from flask_jwt import jwt_required


class Store(Resource):

	@jwt_required()
	def get(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			return store.json(), 200
		else:
			return {"message" : "Sorry the store doesn't exist on our database"},401

	@jwt_required()
	def post(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			return {"message" : f" The  store {name} already exist"}
		else:
			try:
				store = StoreModel(name)
				store.save_to_db()
			except:
				return {"message" : "an error on our part occured"}, 500
		return store.json(), 201

	@jwt_required()
	def delete(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			store.delete_from_db()
		return {"message" : "The store is deleted"}, 201


class StoreList(Resource):
	@jwt_required()
	def get(self):
		return {"Stores" : [store.json() for store in StoreModel.query.all()]}

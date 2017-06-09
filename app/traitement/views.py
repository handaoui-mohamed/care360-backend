from app import db, api, authorization
from flask_restplus import Resource
from flask import abort, g
from app.user.models import User
from app.user.decorators import login_required
from models import Traitement
from serializers import traitement_model

traitement_api = api.namespace('traitements', description='For showing Patient traitement')


@traitement_api.route('/<string:userId>')
class Traitements(Resource):
	@traitement_api.expect(authorization)
	@login_required
	def get(self, userId):
		"""
		Returns all traitements.
		"""
		if User.query.get(userId) is None:
			return {'message': "L\'utilisateur n\'exists pas!"}, 404
		return {'elements': [element.to_json() for element in Traitement.query.filter_by(user_id=userId).all()]}

	@traitement_api.expect(authorization, traitement_model)
	@login_required
	def post(self,userId):
		"""
		Adds a new traitement.
		"""
		data = api.payload
		content = data.get('content')

		if User.query.get(userId) is None:
			return {'message': "L\'utilisateur n\'exists pas!"}, 404

		traitement = Traitement(content=content,user_id=userId)
		db.session.add(traitement)
		db.session.commit()
		return {'element': traitement.to_json()}, 201

@traitement_api.route('/<int:id>')
class TraitementById(Resource):
	@traitement_api.expect(authorization, traitement_model)
	@login_required
	def put(self,id):
		"""
		Modify a traitement.
		"""
		data = api.payload
		content = data.get('content')
		done = data.get('done')

		traitement = Traitement.query.get(id)

		if traitement is None:
			return {'message': "Le traitement n\'exists pas!"}, 404

		traitement.content = content
		traitement.done = done

		db.session.add(traitement)
		db.session.commit()
		return {'element': traitement.to_json()}, 201
	
	@traitement_api.expect(authorization)
	@login_required
	def delete(self,id):
		"""
		Delete a traitement.
		"""		
		traitement = Traitement.query.get(id)

		if traitement is None:
			return {'message': "Le traitement n\'exists pas!"}, 404

		traitement.deleted = True
		db.session.add(traitement)
		db.session.commit()
		return "", 200

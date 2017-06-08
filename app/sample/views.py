from app import db, api, authorization
from flask_restplus import Resource
from flask import abort, g
from app.user.models import User
from app.user.decorators import login_required
from models import Sample
from serializers import sample_model

sample_api = api.namespace('sample', description='For showing Patient samples')


@sample_api.route('/<string:id>')
class Samples(Resource):
	@sample_api.expect(authorization)
	@login_required
	def get(self, id):
		"""
		Returns all samples.
		"""
		if User.query.get(id) is None:
			return {'message': "L\'utilisateur n\'exists pas!"}, 404
		return {'elements': [element.to_json() for element in Sample.query.filter_by(user_id=id).all()]}

	@sample_api.expect(authorization, sample_model)
	@login_required
	def post(self,id):
		"""
		Adds a new case.
		"""
		data = api.payload
		type = data.get('type')
		value = data.get('value')

		if User.query.get(id) is None:
			return {'message': "L\'utilisateur n\'exists pas!"}, 404

		sample = Sample(type=type,value=value,user_id=id)
		db.session.add(sample)
		db.session.commit()
		return {'element': sample.to_json()}, 201

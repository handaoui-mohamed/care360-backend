from app import db, api, authorization
from flask_restplus import Resource
from flask import abort, g
from app.user.models import User
from app.user.decorators import super_user_required
from models import Case
from serializers import case_model

case_api = api.namespace('cases', description='For showing User cases')

@case_api.route('')
class Cases(Resource):
    def get(self):
        """
        Returns all cases.
        """
        return {'elements': [element.to_json() for element in Case.query.all()]}
    
    @case_api.expect(authorization,case_model)
    @super_user_required
    def post(self):
        """
        Adds a new case.
        """
        data = api.payload
        name = data.get('name')

        if Case.query.filter_by(name=name).first() is not None:
            return {'message': "The case\'s name already exists!"}, 400

        case = Case(name=name)
        db.session.add(case)
        db.session.commit()
        return {'element': case.to_json()}, 201


@case_api.route('/<int:id>')
class CasesById(Resource):
    def get(self, id):
        """
        Returns case by id.
        """
        case = Case.query.get(id)
        if case is None:
            abort(404)
        return {'element': case.to_json()}

    @case_api.expect(authorization,case_model)
    @super_user_required
    def put(self, id):
        """
        Update case's name.
        """
        case = Case.query.get(id)
        if case is None:
            abort(404)

        data = api.payload
        name = data.get('name')

        new_case = False
        existing_case= Case.query.filter_by(name=name).first()
        if (existing_case is None) or (existing_case.id == case.id and not (name == case.name)): new_case =True

        if new_case and name: 
            case.name = name
            db.session.add(case)
            db.session.commit()
            return {'element': case.to_json()}, 201
        return {'message': "The case\'s name already exists!"}, 400

    @case_api.expect(authorization)
    @super_user_required
    def delete(self, id):
        """
        Delete a case.
        """
        case = Case.query.get(id)
        if case is None:
            abort(404)
        db.session.delete(case)
        db.session.commit()
        return '', 204

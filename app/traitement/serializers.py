from app import api
from flask_restplus import fields

traitement_model = api.model('traitement_model', {
    'content': fields.String(required=True),
    'done': fields.Boolean()
})
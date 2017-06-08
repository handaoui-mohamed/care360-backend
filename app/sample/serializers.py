from app import api
from flask_restplus import fields

sample_model = api.model('sample', {
    'type': fields.String(required=True),
    'value': fields.Float(required=True)
})
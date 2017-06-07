from app import api
from flask_restplus import fields

case_model = api.model('Case', {
    'name': fields.String(required=True)
})
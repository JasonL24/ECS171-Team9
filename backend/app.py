from flask import Blueprint
from flask_restful import Api
from resources.Test import Test
from resources.Library import Library

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Test, '/test')
api.add_resource(Library, '/library')
from flask_restful import Resource
from ..ml_src.generate_song import generate_song

class Generate(Resource):
    def get(self):
        generate_song()
        return {"a": "Jason's json"}

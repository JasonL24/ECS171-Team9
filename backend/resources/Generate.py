from flask_restful import Resource
from ..ml_src.generate_song import generate_song

class Generate(Resource):
    def get(self):
        song_id = generate_song()
        return {"song_id": song_id}

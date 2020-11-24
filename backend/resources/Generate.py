from flask_restful import Resource
import sys
from ml_src.generate_song import generate_song

class Generate(Resource):
    def get(self):
        print("Entered generate")
        song_id = generate_song()
        print("song id", song_id)
        return {"song_id": song_id}


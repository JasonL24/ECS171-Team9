from flask_restful import Resource

class Library(Resource):
    def get(self):
        return {"songs": ["happy bday", "song2", "song3"]}
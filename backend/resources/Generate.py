from flask_restful import Resource
## Import your ML file here

class Generate(Resource):
  def get(self):
    ## Run your ML function here
    return {"a": "Jason's json"}
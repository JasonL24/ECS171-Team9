from firebase import firebase
from firebase_admin import credentials, initialize_app
fb = firebase.FirebaseApplication("https://ecs171group9.firebaseio.com", None)

cred = credentials.Certificate('./ml_src/ecs171group9-58247794b74e.json')
initialize_app(cred, {'storageBucket': 'ecs171group9.appspot.com'})

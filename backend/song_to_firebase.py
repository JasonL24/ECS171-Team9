from firebase_admin import credentials, initialize_app, storage

# Init firebase with your credentials
cred = credentials.Certificate("YOUR DOWNLOADED CREDENTIALS FILE (JSON)")
initialize_app(cred, {'storageBucket': 'YOUR FIREBASE STORAGE PATH (without gs://)'})

# Put your local file path
fileName = "myImage.jpg"
bucket = storage.bucket()
blob = bucket.blob(fileName)
blob.upload_from_filename(fileName)

# Opt : if you want to make public access from the URL
blob.make_public()

print("your file url", blob.public_url)

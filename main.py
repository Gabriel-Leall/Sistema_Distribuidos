import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("C:\Users\Gabriel\Documents\VsCode\sistemas-distribuidos-7p-firebase-adminsdk-fbsvc-d7c5ce6b52.json")
firebase_admin.initialize_app(cred)


db = firestore.client()
import firebase_admin
from firebase_admin import credentials, firestore

# cred = credentials.Certificate("C:\\Users\\Gabriel\\Documents\\VsCode\\sistemas-distribuidos-7p-firebase-adminsdk-fbsvc-d7c5ce6b52.json")
cred = credentials.Certificate("C:\\Users\\erlan\\Documents\\Firebase\\sistemas-distribuidos-7p-firebase-adminsdk-fbsvc-4a714ddf4c.json")

firebase_admin.initialize_app(cred)

db = firestore.client()
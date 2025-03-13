import firebase_admin

from firebase_admin import credentials, firestore

# cred = credentials.Certificate("C:\\Users\\Gabriel\\Documents\\VsCode\\sistemas-distribuidos-7p-firebase-adminsdk-fbsvc-d7c5ce6b52.json")
cred = credentials.Certificate("C:\\Users\\erlan\\Documents\\Firebase\\sistemas-distribuidos-7p-firebase-adminsdk-fbsvc-4a714ddf4c.json")

firebase_admin.initialize_app(cred)

db = firestore.client()

import pyrebase 

firebaseConfig = {
  'apiKey': "AIzaSyBT5cTGRC6pbhXsZYsBiLL3AbEdAIZ7h6Q",
  'authDomain': "sistemas-distribuidos-7p.firebaseapp.com",
  'projectId': "sistemas-distribuidos-7p",
  'storageBucket': "sistemas-distribuidos-7p.appspot.com",  
  'messagingSenderId': "292777470780",
  'appId': "1:292777470780:web:abc5e27c6bffb791a08c39",
  'measurementId': "G-4GWNCES5PJ",
  'databaseURL': ""  
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

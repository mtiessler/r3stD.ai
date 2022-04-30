import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import pyrebase

class FirebaseAPI:
    def __init__(self):
        self.config = {
          "apiKey": "AIzaSyD8yFpLg4QOOrOyVAnatXQ_Aamb7Ezxt7s",
          "authDomain": "hackupc2022-1b331.firebaseapp.com",
          "projectId": "hackupc2022-1b331",
          "storageBucket": "hackupc2022-1b331.appspot.com",
          "databaseURL": "",
          "serviceAccount": "serviceAccountCredentials.json"
        }
        firebase = pyrebase.initialize_app(self.config)
        self.storage = firebase.storage()
        

    def save_images(self, uuid, images_folder_path):
        img_file_names = next(os.walk(images_folder_path), (None, None, []))[2]
        for img_file_name in img_file_names:
            self.storage.child(uuid).child('images').child(img_file_name).put(images_folder_path + img_file_name)

        return True


fb_wrapper = FirebaseAPI()
fb_wrapper.save_images('testUUID', '/home/vant/upc/hackupc2022/images/')
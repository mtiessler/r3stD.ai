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
          "serviceAccount": "C:\\Users\\Max\\Desktop\\hackupc2022\\core\\extras\\serviceAccountCredentials.json"
        }
        firebase = pyrebase.initialize_app(self.config)
        self.storage = firebase.storage()


    def save_images(self, uuid, images_folder_path):
        print(uuid)
        print("Saving model images to /{uuid}/images")
        img_file_names = next(os.walk(images_folder_path), (None, None, []))[2]
        for img_file_name in img_file_names:
            self.storage.child(uuid).child('images').child(img_file_name).put(images_folder_path + img_file_name)

        return True


    def save_model_images(self, uuid, model_images_folder_path):
        print(uuid)
        print("Saving model images to /{uuid}/model_images")
        img_file_names = next(os.walk(model_images_folder_path), (None, None, []))[2]
        for img_file_name in img_file_names:
            self.storage.child(uuid).child('model_images').child(img_file_name).put(model_images_folder_path + img_file_name)

        return True


    def load_image_link(self, uuid):
        return self.storage.child(uuid).child('video_images').child('Frame00000.jpg').get_url('1b1e447b-2372-4bbf-976c-106162caafa2')


    def load_model_image_links(self, uuid):
        return [
            self.storage.child(uuid).child('model_images').child('0.png').get_url('1b1e447b-2372-4bbf-976c-106162caafa2'),
            self.storage.child(uuid).child('model_images').child('1.png').get_url('1b1e447b-2372-4bbf-976c-106162caafa2'),
            self.storage.child(uuid).child('model_images').child('2.png').get_url('1b1e447b-2372-4bbf-976c-106162caafa2'),
            self.storage.child(uuid).child('model_images').child('3.png').get_url('1b1e447b-2372-4bbf-976c-106162caafa2'),
            self.storage.child(uuid).child('model_images').child('4.png').get_url('1b1e447b-2372-4bbf-976c-106162caafa2'),
            self.storage.child(uuid).child('model_images').child('5.png').get_url('1b1e447b-2372-4bbf-976c-106162caafa2'),
            self.storage.child(uuid).child('model_images').child('6.png').get_url('1b1e447b-2372-4bbf-976c-106162caafa2'),
            self.storage.child(uuid).child('model_images').child('7.png').get_url('1b1e447b-2372-4bbf-976c-106162caafa2'),
        ]


#fb_wrapper = FirebaseAPI()
#fb_wrapper.save_images('pol', '/home/vant/upc/hackupc2022/images/')
#print(fb_wrapper.load_image_link('pol'))
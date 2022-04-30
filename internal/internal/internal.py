import imp
from flask import Flask, request
import argparse
import requests
from requests import ConnectionError
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from multiprocessing import Process
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '../static/images'

@app.route("/")
def isalive():
    return 'alive'


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
      f = request.files['file']

      f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
      return 'file uploaded successfully'
    print('Is Alive')

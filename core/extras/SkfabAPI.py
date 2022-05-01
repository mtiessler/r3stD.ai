#!/usr/bin/python3

"""Sample script for uploading to Sketchfab using the V3 API and the requests library."""

import json
from time import sleep

# import the requests library
# http://docs.python-requests.org/en/latest
# pip install requests
import requests
from requests.exceptions import RequestException

##
# Uploading a model to Sketchfab is a two step process
#
# 1. Upload a model. If the upload is successful, the API will return
#    the model's uid in the `Location` header, and the model will be placed in the processing queue
#
# 2. Poll for the processing status
#    You can use your model id (see 1.) to poll the model processing status
#    The processing status can be one of the following:
#    - PENDING: the model is in the processing queue
#    - PROCESSING: the model is being processed
#    - SUCCESSED: the model has being sucessfully processed and can be view on sketchfab.com
#    - FAILED: the processing has failed. An error message detailing the reason for the failure
#              will be returned with the response
#
# HINTS
# - limit the rate at which you poll for the status (once every few seconds is more than enough)
##

'''SKETCHFAB_API_URL = 'https://api.sketchfab.com/v3'
API_TOKEN = '84e9a2409cf94ad9b6907926335ee7ae'
MAX_RETRIES = 50
MAX_ERRORS = 10
RETRY_TIMEOUT = 5  # seconds'''


class SkfabAPI:
    API_TOKEN = '84e9a2409cf94ad9b6907926335ee7ae'
    SKETCHFAB_API_URL = 'https://api.sketchfab.com/v3'
    MAX_RETRIES = 50
    MAX_ERRORS = 10
    RETRY_TIMEOUT = 5

    @staticmethod
    def _get_request_payload(*, data=None, files=None, json_payload=False):
        """Helper method that returns the authentication token and proper content type depending on
        whether or not we use JSON payload."""
        data = data or {}
        files = files or {}
        headers = {'Authorization': f'Token {SkfabAPI.API_TOKEN}'}

        if json_payload:
            headers.update({'Content-Type': 'application/json'})
            data = json.dumps(data)

        return {'data': data, 'files': files, 'headers': headers}


    @staticmethod
    def _upload(model_file: str):
        """
        POST a model to sketchfab.
        This endpoint only accepts formData as we upload a file.
        """
        model_endpoint = f'{SkfabAPI.SKETCHFAB_API_URL}/models'

        # Optional parameters
        data = {
            'name': 'Result model',
            'description': 'Result model from your picture(s)S',
            'tags': ['restbai'],  # Array of tags,
            'license': 'by',  # License slug,
            'isPublished': True,
            'isInspectable': True,  # Allow 2D view in model inspector
        }

        print('Uploading...')

        with open(model_file, 'rb') as file_:
            files = {'modelFile': file_}
            payload = SkfabAPI._get_request_payload(data=data, files=files)

            try:
                response = requests.post(model_endpoint, **payload)
            except RequestException as exc:
                print(f'An error occured: {exc}')
                return

        if response.status_code != requests.codes.created:
            print(f'Upload failed with error: {response.json()}')
            return

        # Should be https://api.sketchfab.com/v3/models/XXXX
        model_url = response.headers['Location']
        print('Upload successful. Your model is being processed.')
        print(f'Once the processing is done, the model will be available at: {model_url}')

        return model_url


    @staticmethod
    def _poll_processing_status(model_url):
        """GET the model endpoint to check the processing status."""
        errors = 0
        retry = 0

        print('Start polling processing status for model')

        while (retry < SkfabAPI.MAX_RETRIES) and (errors < SkfabAPI.MAX_ERRORS):
            print(f'Try polling processing status (attempt #{retry})...')

            payload = SkfabAPI._get_request_payload()

            try:
                response = requests.get(model_url, **payload)
            except RequestException as exc:
                print(f'Try failed with error {exc}')
                errors += 1
                retry += 1
                continue

            result = response.json()

            if response.status_code != requests.codes.ok:
                print(f'Upload failed with error: {result["error"]}')
                errors += 1
                retry += 1
                continue

            processing_status = result['status']['processing']

            if processing_status == 'PENDING':
                print(f'Your model is in the processing queue. Will retry in {SkfabAPI.RETRY_TIMEOUT} seconds')
                retry += 1
                sleep(SkfabAPI.RETRY_TIMEOUT)
                continue
            elif processing_status == 'PROCESSING':
                print(f'Your model is still being processed. Will retry in {SkfabAPI.RETRY_TIMEOUT} seconds')
                retry += 1
                sleep(SkfabAPI.RETRY_TIMEOUT)
                continue
            elif processing_status == 'FAILED':
                print(f'Processing failed: {result["error"]}')
                return False
            elif processing_status == 'SUCCEEDED':
                print(f'Processing successful. Check your model here: {model_url}')
                return True

            retry += 1

        print('Stopped polling after too many retries or too many errors')
        return False


    def upload_model(model_path: str):
        model_url = SkfabAPI._upload(model_path)
        if model_url:
            if SkfabAPI._poll_processing_status(model_url):
                return model_url
            return False
        return False
import requests 
import json


class RbAPI: 
    # Should be treated as a Singleton to exploit cache

    CLIENT_KEY = '0edd140f4fec8e61e66e0af9b89642a6099380deff6fec8921ca07b7ed8a0b2e'
    BASE_URL =  'https://api-us.restb.ai/vision/v2/multipredict'
    DEMO_IMAGE_URL = 'https://demo.restb.ai/images/demo/demo-1.jpg'
    MODEL_FEATURES = 're_features_v3'
    MODEL_APPLIANCES = 're_appliances_v2'
    MODEL_ROOM_TYPE = 're_roomtype_global_v2'
    MODEL_CONDITION = 're_condition' # Score from 1 to 6
    ALL_MODELS = [MODEL_FEATURES, MODEL_APPLIANCES, MODEL_ROOM_TYPE, MODEL_CONDITION]


    def __init__(self):
        # {'IMG_URL': API_RESULT}
        self._cached_requests = {} 

    # Public methods

    def get_features(self, image_url: str = DEMO_IMAGE_URL):
        self._cache(image_url)
        return self._cached_requests[image_url][RbAPI.MODEL_FEATURES]


    def get_appliances(self, image_url: str = DEMO_IMAGE_URL):
        self._cache(image_url)
        return self._cached_requests[image_url][RbAPI.MODEL_APPLIANCES]


    def get_room_type(self, image_url: str = DEMO_IMAGE_URL):
        self._cache(image_url)
        return self._cached_requests[image_url][RbAPI.MODEL_ROOM_TYPE]


    def get_condition(self, image_url: str = DEMO_IMAGE_URL):
        self._cache(image_url)
        return self._cached_requests[image_url][RbAPI.MODEL_CONDITION]


    def get_all_data(self, image_url: str = DEMO_IMAGE_URL):
        self._cache(image_url)
        return self._cached_requests[image_url]

    
    # Private methods

    def _cache(self, image_url: str):
        if image_url not in self._cached_requests:
            self._cached_requests[image_url] = self._get_all_data(image_url)


    def _get_all_data(self, image_url: str, model_ids=ALL_MODELS):
        api_result = self._api_call(image_url, model_ids)
        return None if api_result is None else api_result['solutions']


    def _api_call(self, image_url, model_ids=ALL_MODELS):
        params = {
            'image_url': image_url,
            'model_id': ",".join(model_ids),
            'client_key': RbAPI.CLIENT_KEY
        }

        response = requests.get(RbAPI.BASE_URL, params = params)
        data = json.loads(response.text)

        if data['error'] != 'false':
            return None

        return data['response']
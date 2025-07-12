"""
alder_api_client.py
author: narlock

The client interface for communicating with the Alder API.
Uses the requests module to perform the HTTP requests.
"""

import cfg
import requests
import traceback
import json

from tools.log import Logger

BASE_URL = cfg.ALDER_API_URL

class AlderAPIClient():
    """
    Usage: 
    Import both the AlderAPIClient and the json module.
    Make your HTTP call and retrieve the body as JSON.

    response = AlderAPIClient.get('/user/1') # Performs call and sets response
    body = json.loads(response.text) # Parses text response to Python object

    Now, we can use the body as a Python object. For example, if response.text was:
    {
    "hex": "383838",
    "id": 1,
    "stime": 0,
    "tokens": 0,
    "trivia": 0
    }
    json.loads would parse this into an actual Python object
    {'hex': '383838', 'id': 1, 'stime': 0, 'tokens': 0, 'trivia': 0}
    And we can access each field in the response.
    print(body['hex']) # would print 383838
    """
    
    @staticmethod
    def get(path):
        """
        Performs a HTTP GET request against the Alder API
        given a path. Returns the response.
        """
        url = f'{BASE_URL}{path}'
        try:
            Logger.debug(f'[GET] Request URL: {url}')
            response = requests.get(url, timeout=5)
            Logger.debug(f'[GET] Response {response.status_code}: {response.text}')
            return response
        except Exception as e:
            Logger.error(f'Error during GET {url}: {str(e)}')
            traceback.print_exc()
            return None

    @staticmethod
    def post(path, request_body):
        """
        Performs HTTP POST request against the Alder API
        given the path and optional request body. Returns the
        response.
        """
        url = f'{BASE_URL}{path}'
        try:
            Logger.debug(f'[POST] Request URL: {url}')
            Logger.debug(f'[POST] Request Body: {json.dumps(request_body)}')
            response = requests.post(url, json=request_body, timeout=5)
            Logger.debug(f'[POST] Response {response.status_code}: {response.text}')
            return response
        except Exception as e:
            Logger.error(f'Error during POST {url}: {str(e)}')
            traceback.print_exc()
            return None

    @staticmethod
    def patch(path, request_body):
        """
        Performs HTTP PATCH request against the Alder API
        given the path and optional request body. Returns the
        response.
        """
        url = f'{BASE_URL}{path}'
        try:
            Logger.debug(f'[PATCH] Request URL: {url}')
            Logger.debug(f'[PATCH] Request Body: {json.dumps(request_body)}')
            response = requests.patch(url, json=request_body, timeout=5)
            Logger.debug(f'[PATCH] Response {response.status_code}: {response.text}')
            return response
        except Exception as e:
            Logger.error(f'Error during PATCH {url}: {str(e)}')
            traceback.print_exc()
            return None

    @staticmethod
    def put(path, request_body):
        """
        Performs HTTP PUT request against the Alder API
        given the path and optional request body. Returns the
        response.
        """
        url = f'{BASE_URL}{path}'
        try:
            Logger.debug(f'[PUT] Request URL: {url}')
            Logger.debug(f'[PUT] Request Body: {json.dumps(request_body)}')
            response = requests.put(url, json=request_body, timeout=5)
            Logger.debug(f'[PUT] Response {response.status_code}: {response.text}')
            return response
        except Exception as e:
            Logger.error(f'Error during PUT {url}: {str(e)}')
            traceback.print_exc()
            return None

    @staticmethod
    def delete(path):
        """
        Performs HTTP DELETE against the Alder API given
        the path. Returns the response.
        """
        url = f'{BASE_URL}{path}'
        try:
            Logger.debug(f'[DELETE] Request URL: {url}')
            response = requests.delete(url, timeout=5)
            Logger.debug(f'[DELETE] Response {response.status_code}: {response.text}')
            return response
        except Exception as e:
            Logger.error(f'Error during DELETE {url}: {str(e)}')
            traceback.print_exc()
            return None

"""
alder_api_client.py
author: narlock

The client interface for communicating with the Alder API.
Uses the requests module to perform the HTTP requests.
"""

import cfg
import requests
import traceback

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
        try:
            response = requests.get(f'{BASE_URL}{path}', timeout=1)
            return response
        except Exception as e:
            Logger.error(f'Error occurred during Alder API GET {BASE_URL}{path}: {str(e)}')
            traceback.print_exc()
            return None

    @staticmethod
    def post(path, request_body):
        """
        Performs HTTP POST request against the Alder API
        given the path and optional request body. Returns the
        response.
        """
        try:
            response = requests.post(f'{BASE_URL}{path}', json=request_body, timeout=1)
            return response
        except Exception as e:
            Logger.error(f'Error occurred during Alder API POST {BASE_URL}{path}: {str(e)}')
            traceback.print_exc()
            return None

    @staticmethod
    def patch(path, request_body):
        """
        Performs HTTP PATCH request against the Alder API
        given the path and optional request body. Returns the
        response.
        """
        try:
            response = requests.patch(f'{BASE_URL}{path}', json=request_body, timeout=1)
            return response
        except Exception as e:
            Logger.error(f'Error occurred during Alder API PATCH {BASE_URL}{path}: {str(e)}')
            traceback.print_exc()
            return None

    @staticmethod
    def put(path, request_body):
        """
        Performs HTTP PUT request against the Alder API
        given the path and optional request body. Returns the
        response.
        """
        try:
            response = requests.put(f'{BASE_URL}{path}', json=request_body, timeout=1)
            return response
        except Exception as e:
            Logger.error(f'Error occurred during Alder API PUT {BASE_URL}{path}: {str(e)}')
            traceback.print_exc()
            return None

    @staticmethod
    def delete(path):
        """
        Performs HTTP DELETE against the Alder API given
        the path. Returns the response.
        """
        try:
            response = requests.delete(f'{BASE_URL}{path}', timeout=1)
            return response
        except Exception as e:
            Logger.error(f'Error occurred during Alder API DELETE {BASE_URL}{path}: {str(e)}')
            traceback.print_exc()
            return None

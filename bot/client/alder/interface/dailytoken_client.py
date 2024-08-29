"""
dailytoken_client.py
author: narlock

Alder interface for making HTTP requests to the
dailytoken resource on the Alder API.
"""

import json

from client.alder.alder_api_client import AlderAPIClient
from datetime import datetime

class DailyTokenClient():
    """
    Alder interface for making HTTP requests to the
    dailytoken resource on the Alder API.

    The resource functions section denotes the operations
    that will directly interact with the accomplishment resource.
    These functions will return the full HTTP response
    object.

    The implementation functions section are functions that
    will be used for Bot operations. These functions will
    return a specific field or resource that is requested.
    """

    # =====================
    # RESOURCE FUNCTIONS
    # =====================

    @staticmethod
    def set_dailytoken_entry_for_user(request_body):
        """
        Given the request body, set the daily token
        entry for the user.
        """
        return AlderAPIClient.post('/dailytoken', request_body)
    
    @staticmethod
    def get_dailytoken_entry_for_user(user_id):
        """
        Given the user_id, return the dailytoken entry
        for the user
        """
        return AlderAPIClient.get(f'/dailytoken/{user_id}')
    
    # ========================
    # IMPLEMENTATION FUNCTIONS
    # ========================

    @staticmethod
    def get_user_dailytoken_time_entry(user_id):
        """
        Given the user_id, attempts to retrieve the daily token
        entry for the user. If it is not present, create
        and return.
        """
        get_response = DailyTokenClient.get_dailytoken_entry_for_user(user_id)
        if get_response is None or get_response.status_code == 404:
            return None
        else:
            entry = json.loads(get_response.text)
            date_time_str = entry['date_time']
            date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S")
            return date_time_obj
        
    @staticmethod
    def set_dailytoken_entry_user_current_time(user_id: int, current_time: datetime):
        """
        Constructs and sends set daily token request
        """

        # Construct request body
        request_body = {
            "user_id": user_id,
            "date_time": current_time.isoformat()
        }

        response = DailyTokenClient.set_dailytoken_entry_for_user(request_body)
        return json.loads(response.text)

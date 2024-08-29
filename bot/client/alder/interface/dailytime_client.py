"""
dailytime_client.py
author: narlock

Alder interface for making HTTP requests to the
dailytime resource on the Alder API.
"""

import json

from client.alder.alder_api_client import AlderAPIClient

class DailyTimeClient():
    """
    Alder interface for making HTTP requests to the
    dailytime resource on the Alder API.

    The resource functions section denotes the operations
    that will directly interact with the dailytime resource.
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
    def search_dailytime(request_body):
        """
        Searches based on the criteria provided in the request body.
        Returns the results of that search.
        """
        return AlderAPIClient.post('/dailytime/search', request_body)
    
    @staticmethod
    def create_dailytime_today_for_user(user_id: int):
        """
        Creates a daily time entry for the user provided
        in the `user_id` parameter.
        """
        return AlderAPIClient.post(f'/dailytime/{user_id}', None)
    
    @staticmethod
    def get_dailytime_today_for_user(user_id: int):
        """
        Retrieves the daily time entry for the user on the current
        day with respect to UTC time zone.
        """
        return AlderAPIClient.get(f'/dailytime/{user_id}')
    
    @staticmethod
    def get_dailytime_for_user_specific_date(user_id: int, day: int, month: int, year: int):
        """
        Retrieves the daily time entry for the user on a specific
        date specified by the `day`, `month`, and `year` parameters.
        """
        return AlderAPIClient.get(f'/dailytime?user_id={user_id}&day={day}&month={month}&year={year}')

    # ========================
    # IMPLEMENTATION FUNCTIONS
    # ========================

    @staticmethod
    def add_stime_to_user_dailytime(user_id: str, stime_to_add: int):
        """
        Adds `stime_to_add` to the user's daily time entry with `user_id`. 
        """

        # Construct request body
        request_body = {
            "stime": stime_to_add
        }

        # Perform PATCH request
        return AlderAPIClient.patch(f'/dailytime/{user_id}', request_body)
    
    @staticmethod
    def get_stime_value_for_user_today(user_id: str) -> int:
        """
        Returns the stime field from the user's dailytime entry
        for the current day.
        """
        response = DailyTimeClient.get_dailytime_today_for_user(user_id)
        body = json.loads(response.text)
        return body['stime']
    
    @staticmethod
    def get_top_10_stime_users_today():
        """
        Returns the top 10 stime users for the current day.
        """
        
        # Construct request body
        request_body = {
            "limit": 10
        }

        # Obtain response and return users list
        response = DailyTimeClient.search_dailytime(request_body)
        return json.loads(response.text)
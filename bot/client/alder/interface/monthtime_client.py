"""
monthtime_client.py
author: narlock

Alder interface for making HTTP requests to the
monthtime resource on the Alder API.
"""

import json

from client.alder.alder_api_client import AlderAPIClient

class MonthTimeClient():
    """
    Alder interface for making HTTP requests to the
    monthtime resource on the Alder API.

    The resource functions section denotes the operations
    that will directly interact with the monthtime resource.
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
    def search_monthtime(request_body):
        """
        Searches based on the criteria provided in the request body.
        Returns the results of that search.
        """
        return AlderAPIClient.post('/monthtime/search', request_body)
    
    @staticmethod
    def create_monthtime_current_month_for_user(user_id: int):
        """
        Creates a month time entry for the user provided
        in the `user_id` parameter.
        """
        return AlderAPIClient.post(f'/monthtime/{user_id}', None)
    
    @staticmethod
    def get_monthtime_current_month_for_user(user_id: int):
        """
        Retrieves the month time entry for the user for the
        current month.
        """
        return AlderAPIClient.get(f'/monthtime/{user_id}')
    
    @staticmethod
    def get_monthtime_for_user_specific_date(user_id: int, month: int, year: int):
        """
        Retrieves the month time entry for the user on a specific date
        specified by the `month` and `year` parameters.
        """
        return AlderAPIClient.get(f'/monthtime?user_id={user_id}&month={month}&year={year}')
    
    # ========================
    # IMPLEMENTATION FUNCTIONS
    # ========================

    @staticmethod
    def add_stime_to_user_monthtime(user_id: str, stime_to_add: int):
        """
        Adds `stime_to_add` to the user's month time entry with `user_id`
        """

        # Construct request body
        request_body = {
            "stime": stime_to_add
        }

        # Perform PATCH request
        return AlderAPIClient.patch(f'/monthtime/{user_id}', request_body)
    
    @staticmethod
    def get_stime_value_for_user_current_month(user_id: str) -> int:
        """
        Returns the stime field from the user's monthtime entry
        corresponding to the current month.
        """
        response = MonthTimeClient.get_monthtime_current_month_for_user(user_id)
        body = json.loads(response.text)
        return body['stime']
    
    @staticmethod
    def get_top_10_stime_users_current_month():
        """
        Returns the top 10 stime users for the current month
        """

        # Construct request body
        request_body = {
            "limit": 10
        }

        # Obtain response and return users list
        response = MonthTimeClient.search_monthtime(request_body)
        return json.loads(response.text)

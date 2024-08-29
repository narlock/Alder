"""
streak_client.py
author: narlock

Alder interface for making HTTP requests to the
streak resource on the Alder API.
"""

import json

from client.alder.alder_api_client import AlderAPIClient
from tools.log import Logger

class StreakClient():
    """
    Alder interface for making HTTP requests to the
    streak resource on the Alder API.

    The resource functions section denotes the operations
    that will directly interact with the streak resource.
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
    def get_streak_for_user(user_id):
        """
        Given the user id, return the streak for the user
        """
        return AlderAPIClient.get(f'/streak/{user_id}')
    
    @staticmethod
    def set_streak_for_user(user_id):
        """
        Sets the streak field for the user
        """
        return AlderAPIClient.post(f'/streak/{user_id}', None)
    
    @staticmethod
    def search_streaks(request_body):
        """
        Searches for streak entries based on request body
        """
        return AlderAPIClient.post(f'/streak/search', request_body)
    
    # ========================
    # IMPLEMENTATION FUNCTIONS
    # ========================

    @staticmethod
    def get_streak_entry_for_user(user_id):
        """
        Calls the set streak endpoint to ensure that
        the streak is updated. Then calls the get
        endpoint to return the streak.
        """
        StreakClient.set_streak_for_user(user_id)
        response = StreakClient.get_streak_for_user(user_id)
        return json.loads(response.text)
    
    @staticmethod
    def get_highest_study_streak_for_user(user_id):
        """
        Retrieves the highest_streak_achieved field for a 
        user's streak entry.
        """
        return StreakClient.get_streak_entry_for_user(user_id)['highest_streak_achieved']
    
    @staticmethod
    def get_top_10_highest_streak_users():
        """
        Returns a list of the top 10 users with the
        highest streaks. Denoted by the
        `highest_streak_achieved` column.
        """

        request_body = {
            "search_field": "highest_streak_achieved",
            "limit": 10
        }

        response = StreakClient.search_streaks(request_body)

        if response is None and response.status_code == 404:
            return None
        
        return json.loads(response.text)
    
    @staticmethod
    def get_top_10_current_streak_users():
        """
        Returns a list of the top 10 users with the
        highest streaks. Denoted by the
        `current_streak` column.
        """

        request_body = {
            "search_field": "current_streak",
            "limit": 10
        }

        response = StreakClient.search_streaks(request_body)

        if response is None and response.status_code == 404:
            return None
        
        return json.loads(response.text)
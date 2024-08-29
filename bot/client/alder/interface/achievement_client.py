"""
achievement_client.py
author: narlock

Alder interface for making HTTP requests to the
achievement resource on the Alder API.
"""

import json

from client.alder.alder_api_client import AlderAPIClient

class AchievementClient():
    """
    Alder interface for making HTTP requests to the
    achievement resource on the Alder API.

    The resource functions section denotes the operations
    that will directly interact with the user resource.
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
    def get_achievements_for_user(user_id):
        """
        Given the user_id, returns all of the achievements
        for the user.
        """
        return AlderAPIClient.get(f'/achievements/{user_id}')
    
    @staticmethod
    def create_achievement_entry(request_body):
        """
        Given the request body, create the achievement
        entry.
        """
        return AlderAPIClient.post('/achievements', request_body)

    # ========================
    # IMPLEMENTATION FUNCTIONS
    # ========================

    @staticmethod
    def get_achievements_for_user_content(user_id):
        """
        Given the user_id, returns the list of achievement ids
        for the user
        """
        response = AchievementClient.get_achievements_for_user(user_id)
        if response is None or response.status_code == 404:
            return []
        else:
            achievements = json.loads(response.text)
            return [item['id'] for item in achievements]
    
    @staticmethod
    def add_user_achievement_id(user_id: int, achievement_id: int):
        """
        Adds the achievement id to the user's achievements.
        """

        # Construct request body
        request_body = {
            "id": achievement_id,
            "user_id": user_id
        }

        # Add the achievement
        return AchievementClient.create_achievement_entry(request_body)
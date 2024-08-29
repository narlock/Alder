"""
accomplishment_client.py
author: narlock

Alder interface for making HTTP requests to the
accomplishment resource on the Alder API.
"""

import json

from client.alder.alder_api_client import AlderAPIClient

class AccomplishmentClient():
    """
    Alder interface for making HTTP requests to the
    accomplishment resource on the Alder API.

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
    def get_accomplishments_for_user(user_id):
        """
        Given the user_id, returns all of the accomplishments
        that match the user_id.
        """
        return AlderAPIClient.get(f'/accomplishments/{user_id}')
    
    @staticmethod
    def create_accomplishment_entry(request_body):
        """
        Given a request_body, creates an accomplishment
        for the user.
        """
        return AlderAPIClient.post(f'/accomplishments', request_body)
    
    # ========================
    # IMPLEMENTATION FUNCTIONS
    # ========================

    @staticmethod
    def get_accomplishments_for_user_content(user_id):
        """
        Given the user_id, returns the list of accomplishments
        for the user.
        """
        response = AccomplishmentClient.get_accomplishments_for_user(user_id)
        if response is None or response.status_code == 404:
            return []
        else:
            accomplishments = json.loads(response.text)
            return [item['msg'] for item in accomplishments]
    
    @staticmethod
    def add_user_accomplishment(user_id: int, accomplishment: str):
        """
        Adds the accomplishment `accomplishment` to the user
        with `user_id`.
        """

        # Construct request body
        request_body = {
            "user_id": user_id,
            "msg": accomplishment
        }

        # Add the accomplishment
        return AccomplishmentClient.create_accomplishment_entry(request_body)
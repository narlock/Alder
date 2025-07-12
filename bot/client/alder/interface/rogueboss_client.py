"""
rogueboss_client.py
author: narlock

Alder interface for making HTTP requests to the
rb resource on the Alder API.
"""

import json
import traceback

from client.alder.alder_api_client import AlderAPIClient

class RbClient():
    """
    Alder interface for making HTTP requests to the
    rb resource on the Alder API.

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
    def get_top_rogue_boss_users(limit: int):
        """
        Get the top rogue boss users given the limit
        where the limit is the number of users to
        return.
        """
        return AlderAPIClient.get(f'/rb/top?limit={limit}')
    
    @staticmethod
    def get_rogue_boss_user(user_id: int):
        """
        Gets the rogue boss user for the user_id
        """
        return AlderAPIClient.get(f'/rb/{user_id}')
    
    @staticmethod
    def create_rogue_boss_user(user_id: int, rbtype: str):
        """
        Creates a rogue boss profile given user_id and
        rbtype
        """

        # Construct request body
        request_body = {
            "user_id": user_id,
            "rbtype": rbtype
        }

        # Make API call
        return AlderAPIClient.post(f'/rb', request_body)
    
    @staticmethod
    def add_xp_to_rogue_boss_user(user_id, xp_to_add):
        """
        Adds xp to the rogue boss user given the user_id
        and the request body
        """

        # Construct request body
        request_body = {
            "xp": int(xp_to_add)
        }

        # Make API call
        return AlderAPIClient.patch(f'/rb/{user_id}/xp', request_body)
    
    @staticmethod
    def update_rogue_boss_user(user_id, request_body):
        """
        Update the rogue boss user given the user_id
        and the request body
        """
        return AlderAPIClient.patch(f'/rb/{user_id}', request_body)

    # ========================
    # IMPLEMENTATION FUNCTIONS
    # ========================

    @staticmethod
    def get_top_10_rogue_boss_users():
        """
        Returns the top 10 rogue boss users
        """
        response = RbClient.get_top_rogue_boss_users(10)
        
        # Return empty list if not a valid response
        if response is None or response.status_code == 404:
            return []
        
        # Return list of users
        return json.loads(response.text)
    
    @staticmethod
    def update_rogue_boss_user_rbtype(user_id: int, rbtype: str):
        """
        Updates the rogue boss user rbtype given user_id
        and rbtype
        """

        # Construct request body
        request_body = {
            "rbtype": rbtype
        }

        # Update rogue boss user
        return RbClient.update_rogue_boss_user(user_id, request_body)

    @staticmethod
    def update_rogue_boss_user_model(user_id: int, model: int):
        """
        Updates the rogue boss user model given user_id
        and model
        """

        # Construct request body
        request_body = {
            "model": model
        }

        # Update rogue boss user
        return RbClient.update_rogue_boss_user(user_id, request_body)
    
    @staticmethod
    def get_rogue_boss_user_purchased_models(user_id):
        """
        Gets the rogue boss user's purchased models
        """
        response = RbClient.get_rogue_boss_user(user_id)
        body = json.loads(response.text)
        return body['purchased_models']


    @staticmethod
    def add_purchased_model_to_rogue_boss_user(user_id: int, model: int):
        """
        Adds the model to the rogue boss user's purchased models list.
        """
        
        # Get and add purchased models
        purchased_models = RbClient.get_rogue_boss_user_purchased_models(user_id)
        purchased_models = f'{purchased_models},{model}'

        # Construct request body
        request_body = {
            "purchased_models": purchased_models
        }

        # Update rogue boss user
        return RbClient.update_rogue_boss_user(user_id, request_body)
    
    @staticmethod
    def get_rogue_boss_user_content(user_id: int):
        """
        Get Rogue Boss Content for Rogue Boss User
        """
        response = RbClient.get_rogue_boss_user(user_id)

        if response is None or response.status_code == 404:
            return None

        body = json.loads(response.text)
        return body
    
    @staticmethod
    def get_rogue_boss_level(user_id: int) -> int:
        """
        Retrieves the user's rogue boss level. If they do not have
        an entry in the table, this function will return 0.
        """
        rb_user = RbClient.get_rogue_boss_user(user_id)
        if rb_user is None or rb_user.status_code == 404:
            return 0
        else:
            try:
                rb_user = json.loads(rb_user.text)
                return 1 if rb_user['xp'] < 9 else round(rb_user['xp'] ** 0.317)
            except Exception as e:
                traceback.print_exc()
                return 0
            
    @staticmethod
    def get_rogue_boss_level_and_xp(user_id: int):
        """
        Retrieves the user's rogue boss level and xp value.
        If they do not have an entry in the table, this
        function will return 0 for both of the values.
        """
        rb_user = RbClient.get_rogue_boss_user(user_id)
        if rb_user is None or rb_user.status_code == 404:
            return 0, 0
        else:
            try:
                rb_user = json.loads(rb_user.text)
                rb_level = 1 if rb_user['xp'] < 9 else round(rb_user['xp'] ** 0.317)
                return rb_level, rb_user['xp']
            except Exception as e:
                traceback.print_exc()
                return 0, 0


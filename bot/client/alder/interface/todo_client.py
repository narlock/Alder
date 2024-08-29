"""
todo_client.py
author: narlock

Alder interface for making HTTP requests to the
todo resource on the Alder API.
"""

import json

from client.alder.alder_api_client import AlderAPIClient

class TodoClient():
    """
    Alder interface for making HTTP requests to the
    todo resource on the Alder API.

    The resource functions section denotes the operations
    that will directly interact with the todo resource.
    These functions will return the full HTTP response
    object.
    """

    # =====================
    # RESOURCE FUNCTIONS
    # =====================

    @staticmethod
    def update_todo_item_name(id: int, new_item_name: str):
        """
        Updates an existing todo item's name
        """

        # Construct request body
        request_body = {
            "item_name": new_item_name
        }

        # Update the todo item
        return AlderAPIClient.patch(f'/todo/{id}', request_body)
    
    @staticmethod
    def create_todo_item(user_id: int, item_name: str):
        """
        Creates a todo item given user_id and item_name.
        """

        # Construct request body
        request_body = {
            "user_id": user_id,
            "item_name": item_name
        }

        # Create the todo item
        return AlderAPIClient.post(f'/todo', request_body)
    
    @staticmethod
    def complete_todo_item(id: int):
        """
        Completes the todo item given its ID
        """
        return AlderAPIClient.post(f'/todo/{id}/complete', None)
    
    @staticmethod
    def get_incomplete_todo_items_for_user(user_id: int):
        """
        Retrieves the todo items for the user that do not have
        a completed date
        """
        return AlderAPIClient.get(f'/todo/incomplete/{user_id}')
    
    @staticmethod
    def get_incomplete_todo_items_for_user_content(user_id: int):
        """
        Returns the content of receiving the incomplete todo item
        """
        response = TodoClient.get_incomplete_todo_items_for_user(user_id)
        if response is None or response.status_code == 404:
            return []
        else:
            return json.loads(response.text)
    
    @staticmethod
    def get_complete_todo_items_for_user(user_id: int):
        """
        Retrieves the todo items for the user that have
        a completed date
        """
        return AlderAPIClient.get(f'/todo/complete/{user_id}')
    
    @staticmethod
    def get_complete_todo_items_for_user_content(user_id: int):
        """
        Returns the content of receiving the incomplete todo item
        """
        response = TodoClient.get_complete_todo_items_for_user(user_id)
        if response is None or response.status_code == 404:
            return []
        else:
            return json.loads(response.text)
    
    @staticmethod
    def delete_todo_item(id: int):
        """
        Delete a todo item by its id
        """
        return AlderAPIClient.delete(f'/todo/{id}')

    @staticmethod
    def delete_old_completed_todo_items_for_user(user_id: int):
        """
        Deletes all of the completed todo items for the user
        that are older than a day.
        """
        return AlderAPIClient.delete(f'/todo/complete/{user_id}')
    
    @staticmethod
    def delete_all_todo_items_for_user(user_id: int):
        """
        Deletes all of the todo items for the user
        """
        return AlderAPIClient.delete(f'/todo/all/{user_id}')
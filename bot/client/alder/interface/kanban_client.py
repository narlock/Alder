"""
kanban_client.py
author: narlock

Alder interface for making HTTP requests to the
kanban resource on the Alder API.
"""

import json

from client.alder.alder_api_client import AlderAPIClient

class KanbanClient():
    """
    Alder interface for making HTTP requests to the
    accomplishment resource on the Alder API.

    The resource functions section denotes the operations
    that will directly interact with the accomplishment resource.
    These functions will return the full HTTP response
    object.
    """

    @staticmethod
    def update_kanban_item_details(id: int, request_body):
        """
        Updates the kanban item details given the id and request body
        """
        return AlderAPIClient.patch(f'/kanban/{id}', request_body)
    
    @staticmethod
    def get_user_kanban_items_by_user_id(user_id: int):
        """
        Retrieves the kanban items by the user_id
        """
        return AlderAPIClient.get(f'/kanban/user/{user_id}')
    
    @staticmethod
    def get_user_kanban_items_by_user_id_content(user_id):
        """
        Retrieves the content of the kanban items by user_id
        """
        response = KanbanClient.get_user_kanban_items_by_user_id(user_id)
        
        if response is None or response.status_code == 404:
            return None
        
        return json.loads(response.text)
    
    @staticmethod
    def get_user_kanban_items_by_tag(user_id: int, tag_name: str):
        """
        Retrieves the kanban items by the user_id that match
        the tag_name
        """
        return AlderAPIClient.get(f'/kanban/user/{user_id}/tag/{tag_name}')
    
    @staticmethod
    def get_user_kanban_items_by_tag_content(user_id: int, tag_name: str):
        """
        Retrieves the content of kanban items by tag for the user_id and tag_name
        """
        response = KanbanClient.get_user_kanban_items_by_tag(user_id, tag_name)

        if response is None or response.status_code == 404:
            return None
        
        return json.loads(response.text)
    
    @staticmethod
    def move_kanban_item_column(id: int, user_id: int, column=None):
        """
        Moves the kanban item based on the column attribute. If no
        column is provided, the item will be moved to the next column
        if applicable.
        """

        # Construct request body
        request_body = {
            'user_id': user_id
        }
        
        if column is not None:
            request_body['column'] = column

        # Make API request
        return AlderAPIClient.post(f'/kanban/{id}', request_body)
    
    @staticmethod
    def create_kanban_item(user_id: int, item_name: str, priority_number: int = None, tag_name: str = None, velocity: int = None):
        """
        Creates a kanban item based on the given criteria.

        Required: id, user_id, and item_name
        Optional: priority_number, tag_name, and velocity
        """

        # Construct request body
        request_body = {
            'user_id': user_id,
            'item_name': item_name
        }

        if priority_number is not None:
            request_body['priority_number'] = priority_number

        if tag_name is not None:
            request_body['tag_name'] = tag_name

        if velocity is not None:
            request_body['velocity'] = velocity

        # Make API request
        return AlderAPIClient.post('/kanban', request_body)

    @staticmethod
    def delete_user_kanban_item(user_id: int, id: int):
        """
        Given the user id and the id of the kanban item, delete
        the kanban item.
        """
        return AlderAPIClient.delete(f'/kanban/user/{user_id}/{id}')
    
    @staticmethod
    def delete_completed_user_kanban_items(user_id: int):
        """
        Given the user's user id, delete all of their
        kanban items that are in the 'done' column.
        """
        return AlderAPIClient.delete(f'/kanban/user/{user_id}')
    
    @staticmethod
    def update_kanban_details_with_priority_tag_velocity(id: int, user_id: int, item_name: str, priority_number: int, tag_name: str, velocity: int):
        """
        Updates the kanban details given the information that is not none.
        id must not be none and at least one of the fields must not be none.
        """

        # Construct request body
        request_body = {
            "user_id": user_id
        }

        if item_name is not None:
            request_body['item_name'] = item_name

        if priority_number is not None:
            request_body['priority_number'] = priority_number

        if tag_name is not None:
            request_body['tag_name'] = tag_name

        if velocity is not None:
            request_body['velocity'] = velocity

        if not request_body:
            raise ValueError("At least one field must be provided to update")
        
        return KanbanClient.update_kanban_item_details(id, request_body)
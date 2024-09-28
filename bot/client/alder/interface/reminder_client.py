"""
reminder_client.py
author: narlock

Alder interface for making HTTP requests to the
reminder resource on the Alder API
"""

import json

from client.alder.alder_api_client import AlderAPIClient

class ReminderClient():
    """
    Alder interface for making HTTP requests to the
    reminder resource on the Alder API.
    """

    @staticmethod
    def get_all_reminders():
        """
        Retrieves all reminders that are in the database
        """
        response = AlderAPIClient.get('/reminder')
        print(response)

        # If the response is None, empty, or not successful, return None
        if not response or response.status_code != 200:
            return None
        
        return json.loads(response.text)
    
    @staticmethod
    def get_user_reminders(user_id: int):
        """
        Retrieve all reminders for the user denoted by their
        user_id.
        """
        response = AlderAPIClient.get(f'/reminder/user/{user_id}')

        # If the response is None, empty or not successful, return None
        if not response or response.status_code != 200:
            return None
        
        return json.loads(response.text)
    
    @staticmethod
    def get_reminder_by_id(id: int):
        """
        Retrieve a reminder by its unique identifier.
        """
        response = AlderAPIClient.get(f'/reminder/{id}')

        # If the response is None or not successful, return None
        if not response or response.status_code != 200:
            return None
        
        return json.loads(response.text)
    
    @staticmethod
    def create_reminder(user_id: int, title: str, remind_at, repeat_interval = None, repeat_until = None, repeat_count = None):
        """
        Creates a reminder for the user_id called title. Will be reminded at
        remind_at parameter. The reminder will repeat if provided repeat
        criteria.

        Repeat Interval can be 'daily', 'weekly', 'monthly', 'yearly', and a combination of 'mtwhfsu'
        """
        # Create a JSON payload with the provided parameters
        request_body = {
            'user_id': user_id,
            'title': title,
            'remind_at': remind_at,
            'repeat_interval': repeat_interval,
            'repeat_until': repeat_until,
            'repeat_count': repeat_count
        }

        # Remove any keys with None values to avoid sending them in the request body
        request_body = {k: v for k, v in request_body.items() if v is not None}

        # Send the POST request to the '/reminder' endpoint
        response = AlderAPIClient.post('/reminder', request_body)

        # If the response is not successful, return None
        if not response or response.status_code != 201:
            return None

        # Return the response as JSON
        return json.loads(response.text)
    
    @staticmethod
    def delete_reminder_by_id(id: int):
        """
        Deletes a reminder by its id.
        """
        return AlderAPIClient.delete(f'/reminder/{id}')

    @staticmethod
    def update_reminder_date(id: int, remind_date: str):
        """
        Updates the remind_at date for the reminder with the given id.
        The time component of the remind_at field will remain unchanged.
        
        :param id: The unique identifier of the reminder.
        :param remind_date: The new date string (YYYY-MM-DD) to set for the remind_at field.
        """
        # Create the request body with the new remind_at date
        request_body = {
            'remind_at': remind_date  # Only update the date part, leave time unchanged
        }

        # Send the PUT request to the '/reminder/<id>/date' endpoint
        response = AlderAPIClient.put(f'/reminder/{id}/date', request_body)

        print(response)

        # If the response is not successful, return None
        if not response or response.status_code != 200:
            return None

        # Return the response as JSON
        return json.loads(response.text)

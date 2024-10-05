"""
user_client.py
author: narlock

Alder user interface for making HTTP requests to the
user resource on the Alder API.
"""

import json
import discord

from client.alder.alder_api_client import AlderAPIClient
from client.alder.interface.monthtime_client import MonthTimeClient
from client.alder.interface.dailytime_client import DailyTimeClient
from client.alder.interface.streak_client import StreakClient

class UserClient():
    """
    Alder user interface for making HTTP requests to the
    user resource on the Alder API.

    The resource functions section denotes the operations
    that will directly interact with the user resource.
    These functions will return the full HTTP response
    object.

    The helper functions section is to help provide an easier
    interface for implementation functions.

    The implementation functions section are functions that
    will be used for Bot operations. These functions will
    return a specific field or resource that is requested.
    """

    # =====================
    # RESOURCE FUNCTIONS
    # =====================

    @staticmethod
    def search_users(request_body):
        """
        Given the search constraints in request_body, search
        for users that meet the constraints.
        """
        return AlderAPIClient.post('/user/search', request_body)
    
    @staticmethod
    def get_user_by_id(id):
        """
        Given the id, corresponding to the user's Discord ID,
        retrieve information from the user resource for that
        user.
        """
        return AlderAPIClient.get(f'/user/{id}')
    
    @staticmethod
    def create_user(request_body):
        """
        Given a body to create a user, call the API to create
        the user.
        """
        return AlderAPIClient.post('/user', request_body)
    
    @staticmethod
    def overwrite_user(id, request_body):
        """
        Given the id of a current user corresponding to the
        Discord ID. Overwrite the properites of the user given
        the request body.
        """
        return AlderAPIClient.put(f'/user/{id}', request_body)
    
    @staticmethod
    def update_user(id, request_body):
        """
        Given the id corresponding to the user's Discord ID,
        perform a partial update against the user resource.

        This function can be used to update `hex`, `stime`,
        `tokens`, and `trivia` fields.
        """
        return AlderAPIClient.patch(f'/user/{id}', request_body)
    
    @staticmethod
    def delete_user(id):
        """
        Given the id corresponding to the user's Discord ID,
        delete the user resource.
        """
        return AlderAPIClient.delete(f'/user/{id}')
    
    @staticmethod
    def set_timezone(id: str, timezone: str):
        """
        Calls the set timezone endpoint which puts the
        value of {timezone} parameter in the user with
        {id} row.
        """
        # Construct request body
        request_body = {
            "timezone": timezone
        }

        # Perform set timezone operation
        response = AlderAPIClient.put(f"/user/{id}/timezone", request_body)

        if not response or response.status_code == 404:
            return None
        
        return json.loads(response.text)
    
    # =====================
    # HELPER FUNCTIONS
    # =====================

    @staticmethod
    def get_user_profile(id: int):
        """
        Retrieves the user profile by id corresponding
        to the user's Discord ID
        """
        response = UserClient.get_user_by_id(id)
        
        # If the profile was not found, return None
        if response.status_code == 404:
            return None
        
        # Otherwise, return the profile data
        body = json.loads(response.text)
        return body

    @staticmethod
    def get_user_property(id: int, property: str):
        """
        Retrieves the user resource given the corresponding
        discord ID `id`. Returns the property on the user
        resource.
        """
        body = UserClient.get_user_profile(id)

        # return None if body is None
        if body is None:
            return None

        return body[property]
    
    @staticmethod
    def search_top_10_field(field: str):
        """
        Calls the search endpoint to return the top
        10 users with the highest `field` column.
        """
        # Construct request body
        request_body = {
            "limit": 10,
            "sort_field": field
        }

        # Perform search and return response object
        response = UserClient.search_users(request_body)
        return json.loads(response.text)

    # ========================
    # IMPLEMENTATION FUNCTIONS
    # ========================

    @staticmethod
    def get_user_tokens(id: str) -> int:
        """
        Retrieves the user resource given the corresponding
        discord ID `id`. Then returns only the amount of
        tokens that the user has.
        """
        return UserClient.get_user_property(id, 'tokens')
    
    @staticmethod
    def get_user_stime(id: str) -> int:
        """
        Retrieves the user resource given the corresponding
        discord ID `id`. Then returns only the stime column's
        value.
        """
        return UserClient.get_user_property(id, 'stime')
    
    @staticmethod
    def get_user_hex(id: str) -> str:
        """
        Retrieves the user resource given the corresponding
        discord ID `id`. Then returns only the hex column's
        value.
        """
        return UserClient.get_user_property(id, 'hex')
    
    @staticmethod
    def get_discord_user_embed_color(id: str) -> discord.Colour:
        """
        Given the user's hex value, return that hex value as
        a discord.py Colour object.
        """
        hex_string = UserClient.get_user_hex(id)
        hex_integer = int(hex_string, 16)

        red = (hex_integer >> 16) & 0xff
        green = (hex_integer >> 8) & 0xff
        blue = hex_integer & 0xff

        return discord.Colour.from_rgb(red, green, blue)
    
    @staticmethod
    def get_user_trivia(id: str) -> int:
        """
        Retrieves the user resource given the corresponding
        discord ID `id`. Then returns only the hex column's
        value.
        """
        return UserClient.get_user_property(id, 'trivia')

    @staticmethod
    def add_tokens_user(id: str, num_tokens_to_add: int):
        """
        Adds `num_tokens_to_add` to the user with Discord ID
        corresponding to `id`.
        """
        # Retrieve the current amount of tokens
        current_tokens = UserClient.get_user_tokens(id)

        # Calculate total amount of tokens
        total_tokens = current_tokens + num_tokens_to_add

        # Construct request body
        request_body = {
            "tokens": total_tokens
        }

        # Update the user
        UserClient.update_user(id, request_body)

    @staticmethod
    def subtract_tokens_user(id: str, num_tokens_to_subtract: int):
        """
        Subtracts `num_tokens_to_subtract` to the user with Discord ID
        corresponding to `id`.
        """
        # Retrieve the current amount of tokens
        current_tokens = UserClient.get_user_tokens(id)

        # Calculate total amount of tokens
        total_tokens = current_tokens - num_tokens_to_subtract

        # Construct request body
        request_body = {
            "tokens": total_tokens
        }

        # Update the user
        UserClient.update_user(id, request_body)
    
    @staticmethod
    def add_stime_user(id: str, num_stime_to_add: int):
        """
        Adds `num_stime_to_add` to the user with Discord ID
        corresponding to `id`.
        """
        # Retrieve the current amount of stime
        current_stime = UserClient.get_user_stime(id)

        # Calculate total amount of stime
        total_stime = current_stime + num_stime_to_add

        # Construct request body
        request_body = {
            "stime": total_stime
        }

        # Update the user
        UserClient.update_user(id, request_body)

    @staticmethod
    def add_stime_and_tokens_user(id: str, num_stime_to_add: int, num_tokens_to_add: int):
        """
        Adds both `num_stime_to_add` and `num_tokens_to_add` to the user with Discord ID
        corresponding to `id`.
        """
        user = UserClient.get_user_profile(id)
        total_stime = user['stime'] + num_stime_to_add
        total_tokens = user['tokens'] + num_tokens_to_add

        # Construct request body
        request_body = {
            "stime": total_stime,
            "tokens": total_tokens
        }

        # Update the user
        UserClient.update_user(id, request_body)
    
    @staticmethod
    def add_trivia_win_for_user(id: str):
        """
        Adds a single trivia win to the user with Discord ID
        corresponding to `id`.
        """
        # Retrieve the current amount of trivia
        current_trivia = UserClient.get_user_trivia(id)

        # Calculate total amount of trivia
        total_trivia = current_trivia + 1

        # Construct request body
        request_body = {
            "trivia": total_trivia
        }

        # Update the user
        UserClient.update_user(id, request_body)
    
    @staticmethod
    def update_hex_user(id: str, hex: str):
        """
        Updates the `hex` column for the user with Discord ID
        corresponding to `id`.
        """
        # Construct request body
        request_body = {
            "hex": hex
        }

        # Update the user
        UserClient.update_user(id, request_body)
    
    @staticmethod
    def search_top_stime_users():
        """
        Calls the search endpoint to return the top
        10 users with the highest stime column.
        """
        return UserClient.search_top_10_field('stime')
    
    @staticmethod
    def search_top_trivia_users():
        """
        Calls the search endpoint to return the top
        10 users with the highest trivia column
        """
        return UserClient.search_top_10_field('trivia')
    
    @staticmethod
    def search_top_tokens_users():
        """
        Calls the search endpoint to return th top
        10 users with the highest tokens column
        """
        return UserClient.search_top_10_field('tokens')
    
    # ========================
    # SHARED FUNCTIONS
    # ========================

    @staticmethod
    def create_user_if_dne(user_id):
        """
        Checks if the user contains:
        - A user entry in the user table
        - A month time entry in the monthtime table for the current month
        - A daily time entry in the dailytime table for the current month
        - A streak entry in the streak table
        where user_id is the discord ID of the user.
        """

        # Fetch the user
        user = UserClient.get_user_by_id(user_id)
        if user.status_code == 404:
            # If the user is None, create it
            user = UserClient.create_user({
                "id": user_id,
                "hex": "383838",
                "stime": 0,
                "tokens": 0,
                "trivia": 0
            })

        # Fetch the month time entry
        monthtime = MonthTimeClient.get_monthtime_current_month_for_user(user_id)
        if monthtime.status_code == 404:
            # If the monthtime is None, create it
            monthtime = MonthTimeClient.create_monthtime_current_month_for_user(user_id)

        # Fetch the daily time entry
        dailytime = DailyTimeClient.get_dailytime_today_for_user(user_id)
        if dailytime.status_code == 404:
            # If the dailytime is None, create it
            dailytime = DailyTimeClient.create_dailytime_today_for_user(user_id)

        # Fetch the streak entry
        streak = StreakClient.get_streak_for_user(user_id)
        if streak.status_code == 404:
            # If the streak entry is None, create it
            streak = StreakClient.set_streak_for_user(user_id)

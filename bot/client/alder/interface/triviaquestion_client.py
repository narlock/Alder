"""
triviaquestion_client.py
author: narlock

Alder interface for making HTTP requests to the
triviaquestion resource on the Alder API.
"""

import json

from client.alder.alder_api_client import AlderAPIClient

class TriviaQuestionClient():
    """
    Alder interface for making HTTP requests to the
    triviaquestion resource on the Alder API.

    The resource functions section denotes the operations
    that will directly interact with the triviaquestion resource.
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
    def get_random_trivia_question():
        """
        Returns a random trivia question from the
        triviaquestion table.
        """
        return AlderAPIClient.get('/trivia')

    # ========================
    # IMPLEMENTATION FUNCTIONS
    # ========================
    
    @staticmethod
    def get_random_trivia_question_contents():
        """
        Retreives a random trivia question, then returns
        the content of that question
        """
        response = TriviaQuestionClient.get_random_trivia_question()
        return json.loads(response.text)
"""
timezone.py
author: narlock

Interface to change timezone information for a user.
"""

import cfg
import discord
import pytz

from datetime import datetime
from client.alder.interface.user_client import UserClient

class TimeZoneApp():
    def set_timezone(self, interaction: discord.Interaction, timezone: str):
        """
        Sets the user's timezone.
        """

        # Validate the timezone string
        try:
            pytz.timezone(timezone)
        except:
            message = f'The timezone {timezone} is not a valid timezone.\nPlease try again.\n\nExample: America/New_York'
            return cfg.ErrorEmbed.message(message)
        
        # The timezone string is valid. Set it
        try:
            UserClient.set_timezone(interaction.user.id, timezone)
            embed = discord.Embed(title=f'Timezone Changed', color=0xffa500)
            embed.add_field(name='\u200b', value=f'Your timezone has been updated to {timezone}.', inline=False)
            embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
            return embed
        except:
            message = f'An unexpected error occurred'
            return cfg.ErrorEmbed.message(message)
        
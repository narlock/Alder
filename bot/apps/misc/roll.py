"""
roll.py
author: narlock

Simple roll interface for rolling random numbers.
"""

import cfg
import random
import discord

class Roll:
    @staticmethod
    def perform_action(interaction: discord.Interaction, max_roll):
        """
        Rolls a random number between 1 and a maximum number (default 100)
        Usage: !roll [max_roll]
        """
        footer_message = None
        roll_message = 'Unexpected error occurred during /roll command.'
        try:
            max_roll = int(max_roll)

            if max_roll < 1:
                roll_message = 'The maximum roll value must be greater than or equal to 1.'
                footer_message = 'Use the /roll command to try again.'
            elif max_roll > 99999:
                roll_message = 'The maximum roll value cannot exceed 99999.'
                footer_message = 'Use the /roll command to try again.'
            else:
                member = interaction.guild.get_member(interaction.user.id)
                username = member.nick if member.nick is not None else member.name
        
                roll_number = random.randint(1, max_roll)
                roll_message = f"{username} rolled a {roll_number} out of {max_roll}!"
        except ValueError:
            roll_message = 'The maximum roll value must be an integer.'
            footer_message = 'Use the /roll command to try again.'

        embed = discord.Embed(title=f'{roll_message}', color=0xffa500)
        try:
            embed.set_thumbnail(url=f'{interaction.user.avatar.url}')
        except Exception as e:
            embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
        if footer_message is not None:
            embed.add_field(name='\u200b', value=footer_message)
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)

        return embed
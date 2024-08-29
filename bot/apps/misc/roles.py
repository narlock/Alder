"""
roles.py
author: narlock

Interface for role selection using discord buttons.
"""

import cfg
import discord

from tools.log import Logger

class RolesToggleButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='📺 Stream', style=discord.ButtonStyle.blurple)
    async def toggle_stream(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get the member who clicked the button
        member = interaction.user
        role_id = cfg.STREAM_ROLE_ID
        role = interaction.guild.get_role(role_id)
        if role:
            if role in member.roles:
                Logger.info(f'Removing stream role for {member.name}')
                await member.remove_roles(role)
            else:
                Logger.info(f'Adding stream role for {member.name}')
                await member.add_roles(role)
        else:
            Logger.error(f'Error occurred when attempting to adding stream role for {member.name}')
        await interaction.response.defer()

    @discord.ui.button(label='📸 YouTube', style=discord.ButtonStyle.blurple)
    async def toggle_youtube(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get the member who clicked the button
        member = interaction.user
        role_id = cfg.YOUTUBE_ROLE_ID
        role = interaction.guild.get_role(role_id)
        if role:
            if role in member.roles:
                Logger.info(f'Removing youtube role for {member.name}')
                await member.remove_roles(role)
            else:
                Logger.info(f'Adding youtube role for {member.name}')
                await member.add_roles(role)
        else:
            Logger.error(f'Error occurred when attempting to adding youtube role for {member.name}')
        await interaction.response.defer()

    @discord.ui.button(label='🌳 Forest', style=discord.ButtonStyle.blurple)
    async def toggle_forest(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get the member who clicked the button
        member = interaction.user
        role_id = cfg.FOREST_ROLE_ID
        role = interaction.guild.get_role(role_id)
        if role:
            if role in member.roles:
                Logger.info(f'Removing forest role for {member.name}')
                await member.remove_roles(role)
            else:
                Logger.info(f'Adding forest role for {member.name}')
                await member.add_roles(role)
        else:
            Logger.error(f'Error occurred when attempting to adding forest role for {member.name}')
        await interaction.response.defer()

    @discord.ui.button(label='📚 Book Club', style=discord.ButtonStyle.blurple)
    async def toggle_book(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get the member who clicked the button
        member = interaction.user
        role_id = cfg.BOOK_ROLE_ID
        role = interaction.guild.get_role(role_id)
        if role:
            if role in member.roles:
                Logger.info(f'Removing book club role for {member.name}')
                await member.remove_roles(role)
            else:
                Logger.info(f'Adding book club role for {member.name}')
                await member.add_roles(role)
        else:
            Logger.error(f'Error occurred when attempting to adding book club role for {member.name}')
        await interaction.response.defer()
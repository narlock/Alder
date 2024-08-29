"""
deep_focus.py
author: narlock

Deep focus role assign interface.
"""

import cfg
import discord

from tools.log import Logger

class DeepFocus():
    async def toggle_deep_focus(self, interaction: discord.Interaction):
        # Get the member who clicked the button
        member = interaction.user

        # Get the deep focus role ID
        deep_focus_role_id = cfg.DEEP_FOCUS_ROLE_ID

        # Get the deep focus role object
        deep_focus_role = interaction.guild.get_role(deep_focus_role_id)

        if deep_focus_role:
            # Check if the member has the deep focus role
            if deep_focus_role in member.roles:
                # Remove the deep focus role
                await member.remove_roles(deep_focus_role)
                Logger.info(f'Removing deep focus role for {member.name}')
            else:
                # Add the deep focus role
                await member.add_roles(deep_focus_role)
                Logger.info(f'Adding deep focus role for {member.name}')
        else:
            Logger.error(f'Error occurred when attempting to adding deep focus role for {member.name}')
            return 1
        
        return 0
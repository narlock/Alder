"""
rules.py
author: narlock

Interface for providing a Discord rules embed based
on the server rules.
"""

import cfg
import discord

class Rules:
    @staticmethod
    def get_rules_embed(rules_channel):
        """
        Creates rules embed.
        """
        embed = discord.Embed(title='Server Rules', color=0xff3a40)
        embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
        embed.add_field(name='\u200b', value='\n'.join([f"**{i+1}** → {item}" for i, item in enumerate(cfg.RULES)]), inline = False)
        embed.add_field(name='\u200b', value=f'**Refer to {rules_channel.mention} for more information**.', inline = False)
        return embed
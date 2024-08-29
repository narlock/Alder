"""
shopembed.py
author: narlock

Shop embed provides an application interface for changing a user's
embed color (this is the color that appears on the left-hand-side of
a Discord embed message)
"""

import cfg
import discord

from tools.log import Logger
from client.alder.interface.user_client import UserClient

class ShopEmbed():
    def purchase_embed(self, user_id, hex):
        # Ensure that the user has been created
        UserClient.create_user_if_dne(user_id)

        # Fetch user's tokens.
        tokens = UserClient.get_user_tokens(user_id)

        # Update user's hex if they have enough tokens.
        if not tokens >= 1000:
            return cfg.ErrorEmbed.notokens(tokens, 1000)

        # Update user's tokens to subtract 1000.
        UserClient.subtract_tokens_user(user_id, 1000)
        tokens -= 1000

        # Return successful embed.
        UserClient.update_hex_user(user_id, hex)

        # Fetch the caller's hex code
        color = UserClient.get_discord_user_embed_color(user_id)

        embed = discord.Embed(title=f'Purchase successful!', color=color)
        embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
        embed.add_field(name='\u200b', value=f'You have successfully updated your embed color to `{hex}`.\n→ A preview of your color is on this embed.\n→ You now have `{tokens}` :coin: tokens.')
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)

        return embed
            
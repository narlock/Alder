"""
shop.py
author: narlock

Shop embed interface.
"""

import cfg
import discord

class Shop():
    @staticmethod
    def show_shop_options():
        embed = discord.Embed(title="Narlock Shop", color=0xffa500)
        embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
        embed.add_field(name='Profile Customization', value=f':dna: </shopembed:{cfg.SHOP_EMBED_COMMAND_ID}> `[hex]` (1000 :coin: tokens)\n→ Customize profile embed color. (Ex: `/shopcolor FFFFFF`)\n\u200b\n:fire: </shopcolor:{cfg.SHOP_COLOR_COMMAND_ID}> `[#]` (500 :coin: tokens)\n→ Customize your server name color. (Ex: `/shopcolor 1`)', inline=False)
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed
"""
shopcolor.py
author: narlock

Shop color provides an interface for users to purchase Discord roles
with the tokens they earn from focusing in dedicated focus rooms.
"""

import cfg
import discord
import datetime

from tools.log import Logger
from client.alder.interface.user_client import UserClient

COLOR_ROLE_LIST = [
    cfg.COLOR_ROLES['role1'],
    cfg.COLOR_ROLES['role2'],
    cfg.COLOR_ROLES['role3'],
    cfg.COLOR_ROLES['role4'],
    cfg.COLOR_ROLES['role5'],
    cfg.COLOR_ROLES['role6'],
    cfg.COLOR_ROLES['role7'],
    cfg.COLOR_ROLES['role8'],
    cfg.COLOR_ROLES['role9'],
    cfg.COLOR_ROLES['role10'],
    cfg.COLOR_ROLES['role11'],
    cfg.COLOR_ROLES['role12'],
    cfg.COLOR_ROLES['role13'],
    cfg.COLOR_ROLES['role14'],
    cfg.COLOR_ROLES['role15'],
    cfg.COLOR_ROLES['role16']
]

class ShopColor():
    def show_color_shop(self):
        """
        Generates the embed for the shop.
        """
        current_month = datetime.datetime.utcnow().month
        month = cfg.MONTHS[current_month]

        embed = discord.Embed(title=f'Change your name color!', color=0xffa500)
        embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
        embed.add_field(name=f':calendar_spiral: {month} Name Colors', value=f'**━━━━━━━━━━━━━━━**\n` 1` → <@&{COLOR_ROLE_LIST[0]}>\n` 2` → <@&{COLOR_ROLE_LIST[1]}>\n` 3` → <@&{COLOR_ROLE_LIST[2]}>\n` 4` → <@&{COLOR_ROLE_LIST[3]}>\n' +
                        f'` 5` → <@&{COLOR_ROLE_LIST[4]}>\n` 6` → <@&{COLOR_ROLE_LIST[5]}>\n` 7` → <@&{COLOR_ROLE_LIST[6]}>\n` 8` → <@&{COLOR_ROLE_LIST[7]}>\n' +
                        f'` 9` → <@&{COLOR_ROLE_LIST[8]}>\n`10` → <@&{COLOR_ROLE_LIST[9]}>\n`11` → <@&{COLOR_ROLE_LIST[10]}>\n`12` → <@&{COLOR_ROLE_LIST[11]}>\n' +
                        f'`13` → <@&{COLOR_ROLE_LIST[12]}>\n`14` → <@&{COLOR_ROLE_LIST[13]}>\n`15` → <@&{COLOR_ROLE_LIST[14]}>\n`16` → <@&{COLOR_ROLE_LIST[15]}>\n**━━━━━━━━━━━━━━━**', inline=False)
        embed.add_field(name='\u200b', value=f'To purchase a color, use the </shopcolor:{cfg.SHOP_COLOR_COMMAND_ID}> command followed by the color id. (Ex: `/shopcolor 1`).\n→ Purchasing a color role costs 500 :coin: tokens.\n→ Color roles reset every month.', inline=False)
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed

    async def purchase_color(self, member: discord.Member, guild: discord.Guild, choice: int):
        """
        Purchases a specified color and generates embed of purchase
        """
        user_id = member.id

        # Ensure that the user has been created
        UserClient.create_user_if_dne(user_id)

        # Fetch user's tokens.
        tokens = UserClient.get_user_tokens(user_id)

        # Check if they can purchase a color role.
        if not tokens >= 500:
            return cfg.ErrorEmbed.notokens(tokens, 500)
        
        # Update user's tokens to subtract 500
        UserClient.subtract_tokens_user(user_id, 500)
        tokens -= 500

        # Update the user's color role. Ensure that they do not have other color roles.
        color_roles = [
            discord.utils.get(guild.roles, id=COLOR_ROLE_LIST[0]),
            discord.utils.get(guild.roles, id=COLOR_ROLE_LIST[1]),
            discord.utils.get(guild.roles, id=COLOR_ROLE_LIST[2]),
            discord.utils.get(guild.roles, id=COLOR_ROLE_LIST[3]),
            discord.utils.get(guild.roles, id=COLOR_ROLE_LIST[4]),
            discord.utils.get(guild.roles, id=COLOR_ROLE_LIST[5]),
            discord.utils.get(guild.roles, id=COLOR_ROLE_LIST[6]),
            discord.utils.get(guild.roles, id=COLOR_ROLE_LIST[7]),
            discord.utils.get(guild.roles, id=COLOR_ROLE_LIST[8]),
            discord.utils.get(guild.roles, id=COLOR_ROLE_LIST[9]),
            discord.utils.get(guild.roles, id=COLOR_ROLE_LIST[10]),
            discord.utils.get(guild.roles, id=COLOR_ROLE_LIST[11]),
            discord.utils.get(guild.roles, id=COLOR_ROLE_LIST[12]),
            discord.utils.get(guild.roles, id=COLOR_ROLE_LIST[13]),
            discord.utils.get(guild.roles, id=COLOR_ROLE_LIST[14]),
            discord.utils.get(guild.roles, id=COLOR_ROLE_LIST[15])
        ]

        # Get the color role based on choice and ensure the user only has that role
        color_role = color_roles[choice - 1]
        for role in member.roles:
            if role in color_roles and role != color_role:
                await member.remove_roles(role)
        await member.add_roles(color_role)

        # Return successful embed
        embed = discord.Embed(title=f'Successful Role Purchase', color=0xffa500)
        embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
        embed.add_field(name='\u200b', value=f'You have successfully updated your role color to\n<@&{COLOR_ROLE_LIST[choice - 1]}>!.\n→ You now have `{tokens}` :coin: tokens.')
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)

        return embed
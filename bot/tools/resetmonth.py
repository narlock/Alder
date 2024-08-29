"""
resetmonth.py (REFACTORED)
author: narlock

Utility for resetting the server roles at the end of the month.
Currrently, this will query the database for every user that connected
to a focus room during the month, check if they have any of the roles
inside of the ROLE_IDS list, and remove each of the roles from the user.
Once this operation is completed, Alder will write a message in the channel
where reset month was triggered stating that it completed.

TODO handle obtaining top 3 monthly users, award them with their respective
awards for becoming top focus users. Create an automatic message highlighting
them inside of the announcements channel.
"""

import cfg
import json
import discord

from tools.log import Logger
from client.alder.interface.monthtime_client import MonthTimeClient
from client.alder.interface.accomplishment_client import AccomplishmentClient
from client.alder.interface.user_client import UserClient

ROLE_IDS = [
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
    cfg.COLOR_ROLES['role16'],
    cfg.LEVEL_1_ACTIVITY_ROLE,
    cfg.LEVEL_2_ACTIVITY_ROLE,
    cfg.LEVEL_3_ACTIVITY_ROLE,
    cfg.LEVEL_4_ACTIVITY_ROLE,
    cfg.LEVEL_5_ACTIVITY_ROLE,
    cfg.LEVEL_6_ACTIVITY_ROLE,
]

PLACES = [':first_place:', ':second_place:', ':third_place:']
PLACE_AWARD = [200, 100, 50]
class ResetMonth():

    async def reset_month(self, ctx):
        # Get all members in the guild
        guild = ctx.guild
        members_with_roles = []

        # Iterate through each member in the guild
        for member in guild.members:
            # Check if the member has any of the roles in ROLE_IDS
            if any(role.id in ROLE_IDS for role in member.roles):
                members_with_roles.append(member)

        Logger.info(f'MONTH RESET BEGINNING ON {len(members_with_roles)} MEMBERS')

        for member in members_with_roles:
            try:
                Logger.info(f'Attempting to remove month roles for {member.name}')
                # Filter the roles to remove based on ROLE_IDS
                roles_to_remove = [role for role in member.roles if role.id in ROLE_IDS]
                await member.remove_roles(*roles_to_remove)
                Logger.success(f'Member {member.name} roles successfully removed!')
            except Exception as e:
                Logger.error(f'An unexpected error was thrown during reset month for user {member.id}: {e}')

        await ctx.send('Narlock Month Reset Complete')
    
    async def reset_month(self, guild: discord.Guild, month, year):
        # Get all members in the guild
        members_with_roles = []

        # Obtain the members that have monthly roles to remove
        for member in guild.members:
            # Check if the member has any of the roles in ROLE_IDS
            if any(role.id in ROLE_IDS for role in member.roles):
                members_with_roles.append(member)

        # Remove the roles of members that contain them
        Logger.debug(f'MONTH RESET BEGINNING ON {len(members_with_roles)} MEMBERS')
        for member in members_with_roles:
            try:
                Logger.info(f'Attempting to remove month roles for {member.name}')
                # Filter the roles to remove based on ROLE_IDS
                roles_to_remove = [role for role in member.roles if role.id in ROLE_IDS]
                await member.remove_roles(*roles_to_remove)
                Logger.success(f'Member {member.name} roles successfully removed!')
            except Exception as e:
                Logger.error(f'An unexpected error was thrown during reset month for user {member.id}: {e}')
        Logger.success('Month role reset complete')

        # Display top 3 users of the month in announcements channel
        response = MonthTimeClient.search_monthtime({"limit": 3, "date": f'{month}-{year}'})
        if response is None or response.status_code == 404:
            top_3_users = []
        else:
            top_3_users = json.loads(response.text)

        top_month_user_message = f"""
Hey @everyone !

{cfg.MONTHS[month]} is now over, meaning our new top focus leaders will be highlighted! At the end of the month, each top focus leader will earn tokens and more! Thanks again for everyone utilizing this bot for their focus time!

"""
        for index, user in enumerate(top_3_users):
            # Add each user to the top month user message 
            top_month_user_message += f'{PLACES[index]} <@{user['user_id']}>\n'

            # Give accomplishment to the top 3 users
            accomplishment_string = f'{PLACES[index]} Focus {cfg.MONTHS[month]} {year}'
            AccomplishmentClient.add_user_accomplishment(user['user_id'], accomplishment_string)

            # Give tokens to the top 3 users
            UserClient.add_tokens_user(user['user_id'], PLACE_AWARD[index])

        # Append footer
        top_month_user_message += '\nCongratulations to the winners of this month!'

        # Send the message to the announcement channel
        announcements_channel = guild.get_channel(cfg.ANNOUNCEMENT_CHANNEL_ID)
        if announcements_channel is not None:
            await announcements_channel.send(top_month_user_message)

        # Success message
        Logger.success('Narlock Month Reset Complete')

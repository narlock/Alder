"""
roleassign.py (REFACTORED)
author: narlock

Role assign is a utility used for determining if users connected to discord voice
channels should earn an activity role. The more that users spend time in specified
channels, the higher level activity role they will receive.
"""
import cfg
import discord

from tools.log import Logger
from client.alder.interface.monthtime_client import MonthTimeClient

class RoleAssign():
    async def check_role_updates_on_user(self, member: discord.Member, guild: discord.Guild = None):
        Logger.debug(f'Checking for role updates for {member.name}')

        # Get Level Roles for Server
        level_one_role = discord.utils.get(guild.roles, id=cfg.LEVEL_1_ACTIVITY_ROLE)
        level_two_role = discord.utils.get(guild.roles, id=cfg.LEVEL_2_ACTIVITY_ROLE)
        level_three_role = discord.utils.get(guild.roles, id=cfg.LEVEL_3_ACTIVITY_ROLE)
        level_four_role = discord.utils.get(guild.roles, id=cfg.LEVEL_4_ACTIVITY_ROLE)
        level_five_role = discord.utils.get(guild.roles, id=cfg.LEVEL_5_ACTIVITY_ROLE)
        level_six_role = discord.utils.get(guild.roles, id=cfg.LEVEL_6_ACTIVITY_ROLE)

        # Retrieve the user's month time and convert to hours
        month_time = MonthTimeClient.get_stime_value_for_user_current_month(member.id) // 3600

        if month_time < 3:
            # Member should not have any level roles since their monthly hours are less than 3
            await member.remove_roles(level_one_role, level_two_role, level_three_role, level_four_role, level_five_role, level_six_role)
            Logger.debug(f"Ensuring {member.name} does not have a level role.")
        elif month_time >= 3 and month_time < 10:
            # Assign Level 1 Role, unless user already has it, deassign other activity roles
            if level_one_role not in member.roles:
                await member.add_roles(level_one_role)
                await member.remove_roles(level_two_role, level_three_role, level_four_role, level_five_role, level_six_role)
                Logger.debug(f"Assigning {member.name} level one role.")
        elif month_time >= 10 and month_time < 25:
            # Assign Level 2 Role, unless user already has it, deassign other activity roles
            if level_two_role not in member.roles:
                await member.add_roles(level_two_role)
                await member.remove_roles(level_one_role, level_three_role, level_four_role, level_five_role, level_six_role)
                Logger.debug(f"Assigning {member.name} level two role.")
        elif month_time >= 25 and month_time < 60:
            # Assign Level 3 Role, unless user already has it, deassign other activity roles
            if level_three_role not in member.roles:
                await member.add_roles(level_three_role)
                await member.remove_roles(level_one_role, level_two_role, level_four_role, level_five_role, level_six_role)
                Logger.debug(f"Assigning {member.name} level three role.")
        elif month_time >= 60 and month_time < 100:
            # Assign Level 4 Role, unless user already has it, deassign other activity roles
            if level_four_role not in member.roles:
                await member.add_roles(level_four_role)
                await member.remove_roles(level_one_role, level_two_role, level_three_role, level_five_role, level_six_role)
                Logger.debug(f"Assigning {member.name} level four role.")
        elif month_time >= 100 and month_time < 250:
            # Assign Level 5 Role, unless user already has it, deassign other activity roles
            if level_five_role not in member.roles:
                await member.add_roles(level_five_role)
                await member.remove_roles(level_one_role, level_two_role, level_three_role, level_four_role, level_six_role)
                Logger.debug(f"Assigning {member.name} level five role.")
        elif month_time >= 250:
            # Assign Level 6 Role, unless user already has it, deassign other roles
            if level_six_role not in member.roles:
                await member.add_roles(level_six_role)
                await member.remove_roles(level_one_role, level_two_role, level_three_role, level_four_role, level_five_role)
                Logger.debug(f"Assigning {member.name} level six role.")

